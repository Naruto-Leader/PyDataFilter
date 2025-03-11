import pandas as pd
from sqlalchemy.sql import text
from data_handler_base import DataHandlerBase

class DataHandler(DataHandlerBase):
    """ 
    Class to import data into a database 

    Args: session (Session): An instance of the database session object 
    """
    def __init__(self, session):
        super().__init__(session)
        
    def import_data(self, data, table_name):
        """
        Imports data into a database table
        
        Args:
        data (DataFrame): The dataframe that holds the data to import
        table_name (str): The name of the table to create in the database
         
        Returns:
        None
        """
        data.to_sql(table_name, self.session.bind, if_exists='replace', index=False)
        self.session.commit()

    def import_data_from_csv(self, file_path, table_name):
        """
        Imports data from CSV into Pandas DataFrame
        
        Args:
        file_path (str): relative path of the CSV file
        table_name (str): The name of the table to create in the database
         
        Returns:
        None        
        """
        data = pd.read_csv(file_path)
        self.import_data(data, table_name)

    def load_list_to_df(self, db_engine, col_list):
        """
        Imports list of columns from database table into Pandas DataFrame
        
        Args:
        db_engine (Engine): database engine object
        col_list (list): list of columns to import from database table
         
        Returns:
        DataFrame: A Pandas DataFrame containing the data
        """
        df = pd.DataFrame(columns=col_list)
        with db_engine.connect() as conn:
            for col in col_list:
                col_list_result = conn.execute(text("SELECT " + col + " FROM ideal_function"))
                df[col] = col_list_result.fetchall()
                #convert tuples to floats
                for i in range(len(df[col])):
                    df[col][i] = df[col][i][0]

            for col in col_list:
                df[col] = df[col].astype(float)
        return df
    
    def copy_table_to_df(self, db_engine, table_name):
        """
        Load data from the database into a Pandas DataFrame
        
        Args:
        table_name (str): The name of the table to load data from
         
        Returns:
        DataFrame: A Pandas DataFrame containing the data
        """
        with db_engine.connect() as conn:
            data_result = conn.execute(text("SELECT * FROM " + table_name))
        
        df = pd.DataFrame(data_result.fetchall(), columns=data_result.keys())        
        return df
