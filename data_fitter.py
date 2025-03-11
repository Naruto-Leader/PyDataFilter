from sqlalchemy.sql import text
import pandas as pd
import numpy as np

class DataFitter:
    """ 
    Class to fit data using the Sum of Squared Errors method

    Args: engine (Engine): An instance of the database engine object 
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.best_fit_functions = []
    
    def calculate_SSE(y_train, y_ideal):
        """
        Calculate the sum of squared errors between the training data and ideal functions
         
        Args:
        y_train (float): y-coordinate from the training data
        y_ideal (float): y-coordinate from the ideal functions
          
        Returns:
        float: The sum of squared errors between the training data and ideal functions
        """

        return np.sum((y_train - y_ideal)**2)
    
    def load_data(self, table_name):
        """
        Load data from the database using engine object
         
        Args:
        table_name (str): The name of the table to load data from
          
        Returns:
        DataFrame: A Pandas DataFrame containing the data
        """

        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM " + table_name))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    def fit_train_data(self, data_table, ideal_table):
        """
        Finds ideal function that best fits the training function
         
        Args:
        data_table (str): The name of the table that holds the data
        ideal_table (str): The name of the table that holds the ideal functions
          
        Returns:
        None
        """

        # Load data from database to Pandas DataFrame
        df_training = self.load_data(data_table)
        df_ideal = self.load_data(ideal_table)

        # Fit data to ideal functions
        for df_train_col in df_training.columns[1:]:
            best_fit_function = []
            best_sse = float('inf')
            for df_ideal_col in df_ideal.columns[1:]:
                sse = np.sum((df_training[df_train_col] - df_ideal[df_ideal_col])**2)
                if sse < best_sse:
                    best_sse = sse
                    best_fit_function = df_ideal_col
            self.best_fit_functions.append(best_fit_function)

        
    def find_delta_y(self, best_fit_func, best_fit_df, test_data_df):
        """
        Find deviation in Y coordinate between test data and best fit ideal functions
         
        Args:
        best_fit_func (list): A list of the best fit ideal functions
        best_fit_df (DataFrame): A Pandas DataFrame containing the best fit ideal functions x-y coordinates
        test_data_df (DataFrame): A Pandas DataFrame containing the test data x-y coordinates
          
        Returns:
        y_delta_num: A list containing the delta in Y coordinate between test data and best fit ideal functions
        y_delta_func: A list containing the name of the ideal function with the smallest y-coordinate deviation
        """
        # Find deviation in Y coordinate between test data and best fit ideal functions, record the smallest deviation into lists
        y_delta_num = []
        y_delta_func = []
        for test_data_index in range(len(test_data_df)):
            for best_fit_col in best_fit_func[:-1]:
                for best_fit_df_index in range(len(best_fit_df)):
                    if best_fit_df['x'][best_fit_df_index] == test_data_df['x'][test_data_index]:
                        y_delta = abs(best_fit_df[best_fit_col][best_fit_df_index] - test_data_df['y'][test_data_index])
                        y_delta_col = best_fit_col
                        break # When X coodinates match, break loop and compare y deviation
                # Compare the current deviation to the previous smallest deviation
                try:
                    y_delta_small
                except NameError:
                    y_delta_small = y_delta
                    y_delta_col_small = y_delta_col
                else:
                    if y_delta < y_delta_small:
                        y_delta_small = y_delta
                        y_delta_col_small = y_delta_col
            # Store y delta and ideal function name in lists for dataframe
            y_delta_num.append(y_delta_small)
            y_delta_func.append(y_delta_col_small)
            
            # Delete variables for next row of test data
            del y_delta_small
            del y_delta_col_small
        
        return y_delta_num, y_delta_func

        

