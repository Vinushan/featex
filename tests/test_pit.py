"""Tests for the Point-in-Time module."""

import pytest
import pandas as pd
from datetime import datetime

from featex.pit import PointInTimeBuilder


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'user_id': [1, 1, 1, 2, 2, 3],
        'timestamp': pd.date_range('2023-01-01', periods=6, freq='D'),
        'amount': [100, 150, 200, 50, 75, 120]
    })


class TestPointInTimeBuilder:
    """Test PointInTimeBuilder class."""
    
    def test_init_with_string_date(self):
        """Test initialization with string date."""
        pit = PointInTimeBuilder('user_id', 'timestamp', '2023-01-03')
        assert pit.entity_col == 'user_id'
        assert pit.timestamp_col == 'timestamp'
        assert isinstance(pit.observation_date, pd.Timestamp)
    
    def test_init_with_datetime(self):
        """Test initialization with datetime object."""
        date = datetime(2023, 1, 3)
        pit = PointInTimeBuilder('user_id', 'timestamp', date)
        assert isinstance(pit.observation_date, pd.Timestamp)
    
    def test_transform_filters_correctly(self, sample_data):
        """Test that transform filters data correctly."""
        pit = PointInTimeBuilder('user_id', 'timestamp', '2023-01-03')
        result = pit.transform(sample_data)
        
        assert len(result) == 2  # Only records from 01-01 and 01-02
        assert result['timestamp'].max() < pit.observation_date
    
    def test_transform_empty_result(self, sample_data):
        """Test transform with observation date before all data."""
        pit = PointInTimeBuilder('user_id', 'timestamp', '2022-12-31')
        result = pit.transform(sample_data)
        
        assert len(result) == 0
    
    def test_get_latest_values(self, sample_data):
        """Test getting latest values per entity."""
        pit = PointInTimeBuilder('user_id', 'timestamp', '2023-01-04')
        latest = pit.get_latest_values(sample_data)
        
        assert len(latest) == 2  # 2 unique users with data before 2023-01-04
        assert 'amount' in latest.columns
        assert 'user_id' in latest.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
