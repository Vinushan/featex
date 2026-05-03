"""
Point-in-Time (PIT) Dataset Builder

This module provides functionality to create historically accurate,
point-in-time datasets for machine learning without data leakage.
"""

from typing import Optional, List, Union
import pandas as pd
import numpy as np
from datetime import datetime


class PointInTimeBuilder:
    """
    Build point-in-time datasets using only historical data available at a given moment.
    
    This prevents data leakage by ensuring features only use information that would
    have been available at the observation date.
    
    Parameters
    ----------
    entity_col : str
        Name of the column containing entity identifiers (e.g., customer_id, user_id)
    timestamp_col : str
        Name of the column containing timestamps
    observation_date : Union[str, datetime]
        The reference date for the point-in-time snapshot. Only data before this
        date will be included in the output.
    
    Example
    -------
    >>> import pandas as pd
    >>> from featex.pit import PointInTimeBuilder
    >>> 
    >>> data = pd.DataFrame({
    ...     'user_id': [1, 1, 2, 2],
    ...     'timestamp': pd.date_range('2023-01-01', periods=4, freq='D'),
    ...     'amount': [100, 150, 50, 75]
    ... })
    >>> 
    >>> pit = PointInTimeBuilder('user_id', 'timestamp', '2023-01-02')
    >>> pit_data = pit.transform(data)
    """
    
    def __init__(
        self,
        entity_col: str,
        timestamp_col: str,
        observation_date: Union[str, datetime],
    ):
        """Initialize the PointInTimeBuilder."""
        self.entity_col = entity_col
        self.timestamp_col = timestamp_col
        
        if isinstance(observation_date, str):
            self.observation_date = pd.to_datetime(observation_date)
        else:
            self.observation_date = observation_date
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data to only include records before the observation date.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataframe with entity and timestamp columns
        
        Returns
        -------
        pd.DataFrame
            Filtered dataframe containing only historical data
        """
        data = data.copy()
        data[self.timestamp_col] = pd.to_datetime(data[self.timestamp_col])
        
        filtered_data = data[data[self.timestamp_col] < self.observation_date]
        
        return filtered_data.reset_index(drop=True)
    
    def get_latest_values(
        self,
        data: pd.DataFrame,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Get the latest values for each entity as of the observation date.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataframe
        columns : Optional[List[str]]
            Columns to include in output. If None, includes all non-entity columns.
        
        Returns
        -------
        pd.DataFrame
            One row per entity with latest values as of observation date
        """
        filtered_data = self.transform(data)
        
        if columns is None:
            columns = [col for col in filtered_data.columns 
                      if col not in [self.entity_col, self.timestamp_col]]
        
        # Get the most recent record for each entity
        latest = filtered_data.sort_values(self.timestamp_col).groupby(
            self.entity_col
        ).tail(1)
        
        return latest[[self.entity_col] + columns].reset_index(drop=True)
