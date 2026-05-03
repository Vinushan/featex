"""
Feature Engineering Utilities

This module provides tools for aggregating and transforming features
across time windows.
"""

from typing import Callable, Dict, List, Optional, Union
from datetime import timedelta
import pandas as pd
import numpy as np


class FeatureAggregator:
    """
    Aggregate features over time windows for entities.
    
    Provides functionality to compute aggregations like sum, mean, count, etc.
    over specified time windows for machine learning features.
    
    Parameters
    ----------
    entity_col : str
        Name of the entity identifier column
    timestamp_col : str
        Name of the timestamp column
    value_col : str
        Name of the column to aggregate
    
    Example
    -------
    >>> import pandas as pd
    >>> from featex.features import FeatureAggregator
    >>> 
    >>> data = pd.DataFrame({
    ...     'user_id': [1, 1, 1, 2, 2],
    ...     'date': pd.date_range('2023-01-01', periods=5, freq='D'),
    ...     'amount': [100, 150, 200, 50, 75]
    ... })
    >>> 
    >>> agg = FeatureAggregator('user_id', 'date', 'amount')
    >>> 
    >>> # Sum over 7-day windows
    >>> result = agg.aggregate(data, '7D', 'sum')
    """
    
    def __init__(
        self,
        entity_col: str,
        timestamp_col: str,
        value_col: str,
    ):
        """Initialize the FeatureAggregator."""
        self.entity_col = entity_col
        self.timestamp_col = timestamp_col
        self.value_col = value_col
    
    def aggregate(
        self,
        data: pd.DataFrame,
        window: str,
        agg_func: Union[str, Callable],
        observation_date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        """
        Aggregate values over a time window.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataframe with entity, timestamp, and value columns
        window : str
            Time window (e.g., '7D' for 7 days, '1H' for 1 hour)
        agg_func : Union[str, Callable]
            Aggregation function ('sum', 'mean', 'count', 'max', 'min')
            or a custom callable
        observation_date : Optional[pd.Timestamp]
            Reference date for aggregation. If None, uses current date.
        
        Returns
        -------
        pd.DataFrame
            Aggregated features with columns [entity_col, 'timestamp', 'feature_value']
        """
        data = data.copy()
        data[self.timestamp_col] = pd.to_datetime(data[self.timestamp_col])
        
        if observation_date is None:
            observation_date = pd.Timestamp.now()
        
        # Filter data to only include records before observation_date
        data = data[data[self.timestamp_col] <= observation_date]
        
        # Calculate window start date
        window_start = observation_date - pd.to_timedelta(window)
        
        # Filter data within the window
        windowed_data = data[
            (data[self.timestamp_col] > window_start) & 
            (data[self.timestamp_col] <= observation_date)
        ]
        
        # Perform aggregation
        if isinstance(agg_func, str):
            result = windowed_data.groupby(self.entity_col)[
                self.value_col
            ].agg(agg_func).reset_index()
            result.columns = [self.entity_col, f'{self.value_col}_{agg_func}_{window}']
        else:
            result = windowed_data.groupby(self.entity_col)[
                self.value_col
            ].apply(agg_func).reset_index()
            result.columns = [self.entity_col, f'{self.value_col}_custom_{window}']
        
        result['observation_date'] = observation_date
        
        return result
    
    def rolling_features(
        self,
        data: pd.DataFrame,
        windows: List[str],
        agg_funcs: List[str],
        observation_date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        """
        Generate multiple rolling window features.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataframe
        windows : List[str]
            List of time windows
        agg_funcs : List[str]
            List of aggregation functions
        observation_date : Optional[pd.Timestamp]
            Reference date for aggregation
        
        Returns
        -------
        pd.DataFrame
            Dataframe with multiple feature columns
        """
        features = None
        
        for window in windows:
            for func in agg_funcs:
                agg_result = self.aggregate(data, window, func, observation_date)
                
                if features is None:
                    features = agg_result
                else:
                    features = features.merge(
                        agg_result,
                        on=[self.entity_col, 'observation_date'],
                        how='outer'
                    )
        
        return features
