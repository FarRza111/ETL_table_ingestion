import os
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    # filename="basic.log",
)

class FileReader:

    def __init__(self, name: str, encoding = None):
        self.name = name
        self.directory = os.getcwd()
        self.fullpath = os.path.join(self.directory, self.name) if self.name and self.directory else "no data"
        self.encoding = encoding


    def read_file(self):

        mapping = {".xlsx": pd.read_excel, 
                   ".csv": lambda path: pd.read_csv(path, encoding=self.encoding),
                   ".txt": pd.read_csv,
                   ".pkl":pd.read_pickle,
                  
                   }

        _, file_extension = os.path.splitext(self.fullpath)

        if file_extension in mapping:
            try:
                df = mapping[file_extension](self.fullpath)
                return df
                logging.info("Successfull read the data")
            except FileNotFoundError:
                logging.error("File Doe snot exist")
        else:
            logging.warning('File not correct format..')

        return " "

    @staticmethod
    def provide_statistics(data):
        return f"""  # of rows:{len(data)}
  # of columns:{len(data.columns)} 
  # of nulls: {data.isnull().sum().sum()}
  ------------------------------------------"""


if __name__== "__main__":
  filereader =  FileReader("dummy.pkl")
  data = filereader.read_file()
  stat = filereader.provide_statistics(data)
  print(stat)
  print(data)
