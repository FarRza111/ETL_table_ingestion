import os
import pandas as pd
import logging
import pyodbc as odbc

"""
AUTHOR: Fariz Rzayev
"""



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class Config:

    @staticmethod
    def odbc_connection(database_name):
        conn_string = (
            "Driver={};"
            "Host=;"
            "Port=;"
            "AuthMech=;"
            "KrbRealm=;"
            "KrbFQDN=;"
            "KrbServiceName=;"
            "SSL=;"
            "UseSystemTrustStore=;"
            "ServicePrincipalCanonicalization=;"
            f"Database={database_name};"
        )

        try:
            connection = odbc.connect(conn_string, autocommit=True)
            cursor = connection.cursor()
            logging.info(f"Connected to Database Successfully: {database_name}")
            return cursor
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            return None





class Converter:
    
#     def __init__(self, table_name):
#         self.table_name = table_name
#         self.directory = os.getcwd()
#     df = {
#         'id': [1, 2, None],
#         'name': ['Alice', 'Bob', 'Charlie'],
#         'is_active': ["No", "Yes", "UNK"],
#         'score': [10.5, None, 3.7]
#     }
#     data = pd.DataFrame(df)

    data = pd.concat([pd.read_excel(file) for file in os.listdir(os.getcwd()) if re.search("EU_highrisk_flag_list.xlsx", file) ])
    data["country_code"].fillna(" ", inplace = True)

    @staticmethod
    def convert_to_int(column, default=0):
        if pd.api.types.is_float_dtype(column):
            return column.fillna(default).astype(int)
        return column

    @classmethod
    def apply_function(cls):
        for column in cls.data.columns:
            if pd.api.types.is_numeric_dtype(cls.data[column]):
                cls.data[column] = cls.convert_to_int(cls.data[column])
        # print(cls.data.info())
        return cls.data



class Database:
    

    @staticmethod
    def batch_insert_or_update(data: pd.DataFrame, db_name: str, tablename: str, dsn: str):
        if data is None or data.empty:
            logging.warn(
                "Your data is empty, please check whether you use your own external table or data coming from impala")
            return
        conn = odbc.connect(f'DSN={dsn}', autocommit=True)
        cursor = conn.cursor()
        column_names = ", ".join(data.columns)
        value_placeholder = ", ".join(["?"] * data.shape[1])
        insert_query = (
            f"INSERT INTO {db_name}.{tablename} ({column_names}) VALUES ({value_placeholder})"
        )

        values = [tuple(row) for _, row in data.iterrows()]
#         print(values)
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

            
def main():
    
    converter = Converter.data
    Converter.apply_function()
    processed_data = Converter.data
    # print(processed_data)

       
    table_name = "statistics"
    db_name = "sales_schema
  
    type_mapping = {

        "int64": "INT",
        "int32": "INT",
        "object": "STRING"
    }


    columns = [
        f"{col} {type_mapping[str(processed_data[col].dtype)]}"
        for col in processed_data.columns
    ]
    
    
    try:
        sql_query = f"CREATE TABLE IF NOT EXISTS dbname.{table_name} ({', '.join(columns)});"
        dsn = int("Enter your data source string")
        conn = odbc.connect(f'DSN={dsn}', autocommit=True)
        print(sql_query)
        Database.execute_query(conn, sql_query)
        Database.batch_insert_or_update(data=processed_data, 
                                        db_name= db_name 
                                        dsn=dsn,
                                        tablename=table_name)
        logging.info("Successfully Ingested..")
    except Exception as e:
        logging.error(f"Error happened : {e}")
    
    return "..."
    
    

if __name__ == "__main__":
    main()
    
