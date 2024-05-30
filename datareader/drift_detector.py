
import pandas as pd
from scipy.stats import ks_2samp
from datamanager.datamanager import DataManager
import numpy as np 



class DataProfiler:

    def __init__(self, threshold=0.1):

        self.profile = None
        self.threshold = threshold
        self.data_manager = DataManager()

    
    def numeric_metrics(self, group):
        return pd.Series({
           "will include the metrics to be shown for numerical features here"
        })

   
    def non_numeric_metrics(self, group):
        return pd.Series({
            "will include the metrics to be shown for categorical features"
        })

    def create_profile(self, source, source_type='csv', split_method='ratio', split_value=0.8, granularity=None, features=None):

        self.data_manager.load_data(source, source_type) 
        self.data_manager.split_data(split_method, split_value) 

        historical_data = self.data_manager.df_old
        new_data = self.data_manager.df_new
        self.historical_data = historical_data


        if features:
            new_data = new_data[features]

        numeric_cols = new_data.select_dtypes(include=np.number).columns
        non_numeric_cols = new_data.select_dtypes(exclude=np.number).columns

       

        return self.profile
