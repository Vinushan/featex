"""
Utility Functions

This module contains helper functions for common operations.
"""

from typing import Optional
import pandas as pd
import numpy as np


def validate_dataframe(
    data: pd.DataFrame,
    required_cols: list,
    raise_error: bool = True,
) -> bool:
    """
    Validate that required columns exist in dataframe.
    
    Parameters
    ----------
    data : pd.DataFrame
        Dataframe to validate
    required_cols : list
        List of required column names
    raise_error : bool, default=True
        Whether to raise an error if validation fails
    
    Returns
    -------
    bool
        True if validation passes
    
    Raises
    ------
    ValueError
        If required columns are missing and raise_error=True
    """
    missing_cols = [col for col in required_cols if col not in data.columns]
    
    if missing_cols:
        error_msg = f"Missing required columns: {missing_cols}"
        if raise_error:
            raise ValueError(error_msg)
        return False
    
    return True


def fill_missing_entities(
    data: pd.DataFrame,
    entity_col: str,
    timestamp_col: str,
    fill_value: Optional[float] = 0,
) -> pd.DataFrame:
    """
    Fill missing values for entities across timestamps.
    
    For entities that have no records at certain timestamps,
    fill them with the specified value.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe
    entity_col : str
        Name of entity column
    timestamp_col : str
        Name of timestamp column
    fill_value : Optional[float]
        Value to fill missing entries with
    
    Returns
    -------
    pd.DataFrame
        Dataframe with filled values
    """
    data = data.copy()
    data[timestamp_col] = pd.to_datetime(data[timestamp_col])
    
    # Create a complete index with all combinations of entities and timestamps
    entities = data[entity_col].unique()
    timestamps = data[timestamp_col].unique()
    
    complete_index = pd.MultiIndex.from_product(
        [entities, timestamps],
        names=[entity_col, timestamp_col]
    )
    
    # Reindex to include all combinations
    data = data.set_index([entity_col, timestamp_col]).reindex(complete_index)
    
    if fill_value is not None:
        data = data.fillna(fill_value)
    
    return data.reset_index()


def get_data_quality_report(data: pd.DataFrame) -> dict:
    """
    Generate a data quality report for a dataframe.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe
    
    Returns
    -------
    dict
        Dictionary with quality metrics
    """
    report = {
        'total_rows': len(data),
        'total_columns': len(data.columns),
        'memory_usage_mb': data.memory_usage(deep=True).sum() / 1024 ** 2,
        'missing_values': data.isnull().sum().to_dict(),
        'missing_value_pct': (data.isnull().sum() / len(data) * 100).to_dict(),
        'dtypes': data.dtypes.astype(str).to_dict(),
    }
    
    return report
