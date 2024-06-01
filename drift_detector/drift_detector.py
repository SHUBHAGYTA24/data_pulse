from typing import List, Dict, Union

import pandas as pd


class DriftDetector:

    """Calculates drift metrics for user-specified columns and granularity."""

    def __init__(self, old_data: pd.DataFrame, new_data: pd.DataFrame):
        self.old_data = old_data
        self.new_data = new_data
        self.metrics = []

    def set_metrics(self, metrics: List[str]) -> None:

        """Sets the user-specified metrics."""
        self.metrics = metrics


    def _supported_metrics(self, data_type: bool) -> List[str]:

        """Defines the valid drift metrics for a given data type (numerical or categorical)."""
        if data_type: #  for numerical data type
            return [
                'mean', 'median', 'std_dev', 'variance', 'skew',
                'kurtosis', 'min, 'max', 'range', 'iqr'
            ]
        else: # for categorical data type
            return ['mode']  


    def calculate_drift(self, columns: List[str], granularity: Union[str, None] = None) -> Dict:
        """Calculates user-specified drift metrics for specified columns and granularity.

        Args:
            columns: List of column names for which to calculate drift metrics.
            granularity: String specifying how to group data (e.g., 'date', 'store', 'date_store').
                - None (default): Calculate overall drift for each column.
                - 'column_name': Calculate drift for each unique value in the column.

        Returns:
            dict: Dictionary containing drift metrics for each column, metric, and granularity level.
        """

        drift_metrics = {}
        if granularity is None:
            # Calculate overall drift for each column
            drift_metrics = self._calculate_overall_drift(columns)
        else:
            # Calculate drift by granularity level
            for col in columns:
                drift_metrics[col] = self._calculate_granular_drift(col, granularity)

        return drift_metrics

    def _calculate_overall_drift(self, columns: List[str]) -> Dict:

        """Calculates user-specified drift metrics for entire datasets, handling numerical and categorical data."""

        drift_metrics = {}
        for col in columns:
            old_stats = self.old_data[col].describe(percentiles=[0.25, 0.75])
            new_stats = self.new_data[col].describe(percentiles=[0.25, 0.75])
            data_type = pd.api.types.is_numeric_dtype(self.old_data[col])

            drift_metrics[col] = {}
            for metric in self.metrics:
                # Validate user-provided metrics
                if metric not in self._supported_metrics(data_type):
                    raise ValueError(f"Invalid metric '{metric}' for data type '{data_type}'.")

                # Calculate the requested metric based on data type
                if metric == 'mean':
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['mean'] - new_stats['mean'])
                elif metric == 'median':
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['50%'] - new_stats['50%'])
                elif metric == 'std_dev' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['std'] - new_stats.get('std'))
                elif metric == 'variance' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['var'] - new_stats.get('var'))
                elif metric == 'skew' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats.get('skew') - new_stats.get('skew'))
                elif metric == 'kurtosis' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats.get('kurt') - new_stats.get('kurt'))
                elif metric == 'min' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['min'] - new_stats['min'])
                elif metric == 'max' and data_type:
                    drift_metrics[col][f"{metric}_diff"] = abs(old_stats['max'] - new_stats['max'])
                elif metric == 'range' and data_type:
                    # 

        return drift_metrics
                                                                         
    def _calculate_granular_drift(self, column: str, metrics: List[str], granularity: str) -> Dict:

        """Calculates user-specified drift metrics for each unique value within a specified granularity level."""
        grouped_data = self.old_data.groupby(granularity)[column]
        old_stats = grouped_data.describe(percentiles=[0.5])

        grouped_data = self.new_data.groupby(granularity)[column]
        new_stats = grouped_data.describe(percentiles=[0.5])

        drift_by_granularity = {}
        for group in old_stats.index:
            old_values = old_stats.loc[group]
            new_values = new_stats.loc[group] if group in new_stats.index else None

            # Check if data exists for this group in both datasets
            if new_values is not None:
                data_type = pd.api.types.is_numeric_dtype(self.old_data[column])
                drift_by_granularity[group] = {}
                for metric in metrics:
                    # Validate user-provided metrics
                    if metric not in self._supported_metrics(data_type):
                        raise ValueError(f"Invalid metric '{metric}' for data type '{data_type}'.")

                    # Calculate the requested metric based on data type
                    if metric == 'mean_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['mean'] - new_values['mean'])
                    elif metric == 'median_diff':
                        drift_by_granularity[group][metric] = abs(old_values['50%'] - new_values['50%'])
                    elif metric == 'std_dev_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['std'] - new_values.get('std'))
                    elif metric == 'variance_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['var'] - new_values.get('var'))
                    elif metric == 'skew_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values.get('skew') - new_values.get('skew'))
                    elif metric == 'kurtosis_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values.get('kurt') - new_values.get('kurt'))
                    elif metric == 'min_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['min'] - new_values['min'])
                    elif metric == 'max_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['max'] - new_values['max'])
                    elif metric == 'range_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['max'] - new_values['max'])
                    elif metric == 'iqr_diff' and data_type:
                        drift_by_granularity[group][metric] = abs(old_values['75%'] - old_values['25%'] - (new_values['75%'] - new_values['25%'] if new_values else 0))
                    # You can add calculations for other metrics here (e.g., categorical metrics)

        return drift_by_granularity
