from data_handler import DataHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

def create_session(db_engine):
    """
    Returns an instance of the database session configuration
    
    Args:
    db_engine (Engine): An instance of the database engine object
         
    Returns:
    session_instance (Session): An instance of the database session 
                                configuration
    """
    base = declarative_base()
    base.metadata.create_all(db_engine)
    session = sessionmaker(bind=db_engine)
    session_instance = session()
    return session_instance

def test_can_load_list_to_df():
    """ 
    Tests that the function to load a list of columns from 
    the database to a dataframe works

    Args:
    None

    Returns:
    None
    """
    # Create a SQLite database engine
    db_engine = create_engine('sqlite:///data.db')
    # Create a session
    session_instance = create_session(db_engine)
    # Create model to move data to database
    data = DataHandler(session_instance)
    # create random list of columns from ideal function table
    col_list = ['y1', 'y2', 'y3']
    test_df = data.load_list_to_df(db_engine, col_list)
    for col in col_list:
        assert col in test_df.columns

    