import pandas as pd
from unittest.mock import patch

from data_pulse.drift_detector.drift_detector import DriftDetector


@patch('drift_detector._calculate_metrics')
def test_calculate_drift_overall(mock_calculate_metrics):
    df1 = pd.DataFrame({'col1': [1, 2, 3]})
    df2 = pd.DataFrame({'col1': [4, 5, 6]})
    detector = DriftDetector(df1, df2)
    detector.metrics = ['mean']
    drift_metrics = detector.calculate_drift(['col1'])
    mock_calculate_metrics.assert_called_once_with(df1['col1'], df2['col1'], ['mean'])
    # Assert the actual drift metrics based on your implementation of _calculate_metrics
    assert drift_metrics == {'col1': {'mean_diff': 1.5}}
