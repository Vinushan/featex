"""Tests for the Feature Engineering module."""

import pytest
import pandas as pd

from featex.features import FeatureAggregator


@pytest.fixture
def sample_data():
    """Create sample transaction data."""
    return pd.DataFrame({
        'user_id': [1, 1, 1, 1, 2, 2, 2],
        'date': pd.date_range('2023-01-01', periods=7, freq='D'),
        'amount': [100, 150, 200, 120, 50, 75, 80]
    })


class TestFeatureAggregator:
    """Test FeatureAggregator class."""
    
    def test_init(self):
        """Test initialization."""
        agg = FeatureAggregator('user_id', 'date', 'amount')
        assert agg.entity_col == 'user_id'
        assert agg.timestamp_col == 'date'
        assert agg.value_col == 'amount'
    
    def test_aggregate_sum(self, sample_data):
        """Test sum aggregation."""
        agg = FeatureAggregator('user_id', 'date', 'amount')
        result = agg.aggregate(
            sample_data,
            '7D',
            'sum',
            observation_date=pd.Timestamp('2023-01-07')
        )
        
        assert len(result) > 0
        assert 'amount_sum_7D' in result.columns
    
    def test_aggregate_mean(self, sample_data):
        """Test mean aggregation."""
        agg = FeatureAggregator('user_id', 'date', 'amount')
        result = agg.aggregate(
            sample_data,
            '7D',
            'mean',
            observation_date=pd.Timestamp('2023-01-07')
        )
        
        assert 'amount_mean_7D' in result.columns
    
    def test_rolling_features(self, sample_data):
        """Test multiple rolling features."""
        agg = FeatureAggregator('user_id', 'date', 'amount')
        result = agg.rolling_features(
            sample_data,
            windows=['3D', '7D'],
            agg_funcs=['sum', 'mean'],
            observation_date=pd.Timestamp('2023-01-07')
        )
        
        assert 'user_id' in result.columns
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
