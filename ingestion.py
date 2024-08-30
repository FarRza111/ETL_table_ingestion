## Importing packages
import os
import logging
import pandas as pd
import pyodbc as odbc
from turtle import TNavigator



def get_data_from_external(file_folder, file_name):
    
    """
    Function to deal with missing values from external table
    """
    full_path = os.path.join(BASE_DIR, file_folder)
    file_path = os.path.join(full_path, file_name)
    
    if os.path.exists(full_path) and os.path.isfile(file_path):
        data = pd.read_excel(file_path)
        
        if not data.empty:
          
            for col in data.select_dtypes(include=['float64']).columns:
                data[col].fillna(0, inplace=True)
                data[col] = data[col].astype(int)
            
            for col in data.select_dtypes(include=['object']).columns:
                data[col].fillna("", inplace = True)
                
            return data
        else:
            print("No Data found in the file.")
    else:
        print(f"File {file_name} does not exist in the directory: {full_path}")
    return None



def get_data_from_hadoop(dsn, query):
    
    """
    Function to fetch the data from hadoop 
    """
    
    try:
        conn = pyodbc.connect(f"DSN={dsn};", autocommit=True)
        data = pd.read_sql(query, conn)
        return data
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
                    
                

def main():
    
    """
    Function to pull all methods ino one main()
    """
    
    selection = input("Do you want to get the data from hadoop or external? ").strip().lower()
    
    global data
    
    if selection == "external":
        file_folder = str(input("which folder your data is in ? "))
        external_table = input("Please enter the name of your file with extension (e.g., eu.xlsx): ").strip()
        data = get_data_from_external(file_folder, external_table)
        if data is not None:
            print(data)
    
    elif selection == "hadoop":
        dsn = str(input("Please enter your data soure name:"))
        query = str(input("Please copy paste your query here : "))
        data = get_data_from_hadoop(dsn,query)
        print(data)
        #### Put your manipulations here before returnning the raw data ####

        return data


class Database:
    
    USER_ID = "Fariz Rza"

    @staticmethod
    def batch_insert_or_update(data: pd.DataFrame = None, db_name: str = None, ds: str = None, dsn=None,
                               tablename: str = None):
        if data is None or data.empty:
            logging.warn(
                "Your data is empty, please check whether you use your own extrnal table or data coming from impala")
            return

        conn = odbc.connect(f'DSN={dsn}', autocommit=True)
        cursor = conn.cursor()
        column_names = ", ".join(data.columns)
        value_placeholder = ", ".join(["?"] * data.columns.size)
        insert_query = (
            f"INSERT INTO {db_name}.{tablename} ({column_names}) VALUES ({value_placeholder}) "
        )
        values = []
        for _, row in data.iterrows():
            values.append(tuple(row.values))
        #     print(insert_query)
        #     print(values)
        cursor.executemany(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()

        
    @staticmethod
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"The error '{e}' occurred")


if __name__ == "__main__":
    
    main()
    
    tablename = "xbtm_test_ext"
                                
    type_mapping = {

        "int64": "INT",
        "int32": "INT",
        "object": "STRING",
#         "float64": "INT"
    }
    
    columns = [
            f"{col} {type_mapping[str(data[col].dtype)]}"
            for col in data.columns
        ]

    
    create_table_sql = f"CREATE TABLE IF NOT EXISTS sale_data.{tablename} ({', '.join(columns)});"
    print(create_table_sql)

    drop_table = f"DROP table if exists arc774_tmexploration_discovery.{tablename}"

    try:
        dsn = "impala 64bit Prod 7.7"
        conn = odbc.connect(f'DSN={dsn}', autocommit=True)
        Database.execute_query(conn, create_table_sql)
#         Database.execute_query(conn, drop_table)
        Database.batch_insert_or_update(data=data, db_name="sales_data", dsn=dsn,
                                        tablename=tablename)
        logging.info(f"Ingestion was done successfully")
    except Exception as e:
        logging.error(f"Error happended : {e}")
        
# select * from sales_data limit 10

# conn = odbc.connect(f'DSN=impala 64bit Prod 7.7', autocommit=True)
# drop_table = f"DROP table if exists sales_data.{tablename}" ##
# print(Database.execute_query(conn, drop_table)) ## delet table in database
