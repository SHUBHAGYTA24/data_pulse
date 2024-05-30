from google.cloud import storage
import pyarrow.parquet as pq
import pandas as pd
from google.cloud import bigquery
from mlutils import dataset
from google.cloud import storage
from io import BytesIO

class DataReader:

    """Class for reading data from various sources and formats."""

    @staticmethod
    def read_csv(source):
        return pd.read_csv(source)

    @staticmethod
    def read_parquet(source):
        return pd.read_parquet(source)

    @staticmethod
    def read_bq(query, connector):

        df = dataset.load(query = query, name = connector)
        return df

    @staticmethod
    def download_blob_from_gcs(source, save_path=None):
        """
        Args:
            source (str): The path to the GCS object in the format 'gs://<bucket>/<object>'.
            save_path (str): The path where the downloaded file should be saved. If None, the file will be read directly into a DataFrame.
        Returns:
            pandas.DataFrame or None: If save_path is None, returns a DataFrame. Otherwise, returns None.
        """

        file_type = source.split('.')[-1]
        
        client = storage.Client()
        blob = storage.Blob.from_string(source, client=client)
        
        # Download the blob to in-memory file and then read it into a pandas DataFrame
        blob_content = blob.download_as_bytes() 
        file_object = BytesIO(blob_content)
        
        
        if file_type == 'parquet':
            df = pd.read_parquet(file_object)
        elif file_type == 'csv':
            df = pd.read_csv(file_object)
        else:
            raise ValueError('Unsupported file type: {}'.format(file_type))
        
        if save_path is not None:
           
            if file_type == 'parquet':
                df.to_parquet(save_path)
            elif file_type == 'csv':
                df.to_csv(save_path)

            return df
        else:
            return df

        