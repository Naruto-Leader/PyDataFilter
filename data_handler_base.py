import pandas as pd

class DataHandlerBase:
    """ 
    Base Class to handle data

    Args: session (Session): An instance of the database session object 
    """
    def __init__(self, session):
        self.session = session

    def import_data(self, data, table_name):
        pass

    def import_data_from_csv(self, file_path, table_name):
        pass

    def load_list_to_df(self, db_engine, col_list):
        pass

    def copy_table_to_df(self, db_engine, table_name):
        pass
