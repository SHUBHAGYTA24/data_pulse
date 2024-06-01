import pandas as pd
from datetime import datetime
from datareader.data_reader import DataReader

class DataManager:
    """
    DataManager class is responsible for loading and managing data.
    
    Attributes:
        df (DataFrame): Complete dataset.
        df_old (DataFrame): Old dataset based on user's input.
        df_new (DataFrame): New dataset based on user's input.
    """
    
    def __init__(self, full_data: pd.DataFrame = None):
        self.full_data = full_data
        self.old_data: pd.DataFrame = None
        self.new_data: pd.DataFrame = None


    def load_data(self, source: str, source_type: str = 'csv', query: str = None, connector: object = None) -> None:

        """
        Load data from the source.
        """
        data_reader = DataReader()
        if source_type == 'csv':

            if "gs://" in source:  
                self.df = data_reader.download_blob_from_gcs(source)
            else:
                self.df = data_reader.read_csv(source)

        elif source_type == 'parquet':
            if "gs://" in source:  
                self.df = data_reader.download_blob_from_gcs(source)
            else:
                self.df = data_reader.read_parquet(source)

        elif source_type == 'bq':
            if query is None or connector is None:
                raise ValueError("For BigQuery source_type, both query and connector must be provided.")
            self.df = data_reader.read_bq(query, connector)
        else:
            raise ValueError("Invalid source_type. Choose from 'csv', 'parquet', or 'bq'.")
        
    def split_data(self, method: str, value: object) -> None:
        """
        Split data into old and new based on the user's input. 
        
        Args:
            method (str): The method to split the data. It can be 'date', 'ratio', 'direct', or 'train_test'.
            value : The value to split the data. It can be a date, a ratio, direct dataframes, or a test size.
        """
        if self.df_old is not None and self.df_new is not None:
            return

        elif method == 'column_value':

            column, split_value = value
            self.df_old = self.df[self.df[column] <= split_value]
            self.df_new = self.df[self.df[column] > split_value]

        elif method == 'ratio':
            split_index = int(len(self.df) * value)
            self.df_old = self.df[:split_index]
            self.df_new = self.df[split_index:]

        elif method == 'direct':
            self.df_old, self.df_new = value
        else:
            raise ValueError("Invalid method. Choose from 'column_value', 'ratio' or 'direct'")