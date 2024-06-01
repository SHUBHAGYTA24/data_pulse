import pandas as pd
from pytest import raises

from drift_detector import DriftDetector


def test_init_same_columns():
    df1 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    df2 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    detector = DriftDetector(df1, df2)
    assert detector.old_data.equals(df1)
    assert detector.new_data.equals(df2)


def test_init_different_columns():
    df1 = pd.DataFrame({'col1': [1, 2, 3]})
    df2 = pd.DataFrame({'col2': [4, 5, 6]})
    with raises(ValueError) as excinfo:
        DriftDetector(df1, df2)
    assert str(excinfo.value) == "DataFrames must have the same columns"
