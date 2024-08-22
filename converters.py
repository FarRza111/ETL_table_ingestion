import os
import pandas as pd

class Converter:

  USER = "Z008374"
  

  def __init__(self, data):
    self.data = data
    # self.current_path = os.getcwd() if os.path.exists(os.getcwd()) else os.path.dirname(os.path.realpath(__file__))

  
  @staticmethod
  def convert_to_int(column, default = 0):
    if column is None:
      return default
    try:
      return int(column)
    except ValueError:
      return default

  @staticmethod
  def convert_to_str(column,default = ''):
    try:
      return str(column)
    except ValueError:
      return default


  
if __name__ == "__main__":

  data = {'col1': [1, 2, None], 
          'col2': [4, 5, 6],
          'col3': ['Far', 'Nizo', None],
          'col4': [12.9, None,5]}

  df = pd.DataFrame(data)
  converter = Converter(data)
  print(df.info())
  print("before")
  df['col1'] = df['col1'].apply(converter.convert_to_int)
  # df['col2'] = df['col2'].apply(converter.convert_to_str)

  print("After")
  print(df.info())
  print(df)



    
  
  
