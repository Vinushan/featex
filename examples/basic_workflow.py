"""
Example: Building a Point-in-Time Dataset

This example demonstrates how to use FeatEx to build a point-in-time
dataset without data leakage.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# For demonstration, we'll use the modules directly
# In practice: from featex.pit import PointInTimeBuilder
import sys
sys.path.insert(0, '../')
from featex.pit import PointInTimeBuilder
from featex.features import FeatureAggregator


def create_sample_transaction_data():
    """Create sample transaction data for demonstration."""
    np.random.seed(42)
    
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    data = []
    
    for user_id in range(1, 11):  # 10 users
        num_transactions = np.random.randint(20, 50)
        transaction_dates = np.random.choice(dates, num_transactions)
        amounts = np.random.uniform(10, 1000, num_transactions)
        
        for date, amount in zip(transaction_dates, amounts):
            data.append({
                'user_id': user_id,
                'transaction_date': date,
                'amount': round(amount, 2)
            })
    
    return pd.DataFrame(data).sort_values('transaction_date')


def example_basic_pit():
    """Example 1: Basic Point-in-Time filtering."""
    print("=" * 60)
    print("Example 1: Basic Point-in-Time Filtering")
    print("=" * 60)
    
    # Create sample data
    transactions = create_sample_transaction_data()
    print(f"\nTotal transactions: {len(transactions)}")
    print(f"Date range: {transactions['transaction_date'].min()} to {transactions['transaction_date'].max()}")
    
    # Create a point-in-time snapshot as of June 30, 2023
    observation_date = '2023-06-30'
    pit_builder = PointInTimeBuilder(
        entity_col='user_id',
        timestamp_col='transaction_date',
        observation_date=observation_date
    )
    
    # Filter to only historical data
    pit_data = pit_builder.transform(transactions)
    print(f"\nTransactions up to {observation_date}: {len(pit_data)}")
    print(f"\nSample data:")
    print(pit_data.head(10))


def example_latest_values():
    """Example 2: Get latest values per entity."""
    print("\n" + "=" * 60)
    print("Example 2: Latest Values Per Entity")
    print("=" * 60)
    
    transactions = create_sample_transaction_data()
    
    observation_date = '2023-06-30'
    pit_builder = PointInTimeBuilder(
        entity_col='user_id',
        timestamp_col='transaction_date',
        observation_date=observation_date
    )
    
    # Get the most recent transaction for each user as of the observation date
    latest = pit_builder.get_latest_values(transactions, columns=['amount'])
    print(f"\nLatest transaction amount per user as of {observation_date}:")
    print(latest.head(10))


def example_feature_aggregation():
    """Example 3: Aggregate features over time windows."""
    print("\n" + "=" * 60)
    print("Example 3: Feature Aggregation Over Time Windows")
    print("=" * 60)
    
    transactions = create_sample_transaction_data()
    
    observation_date = pd.Timestamp('2023-06-30')
    
    # Create a feature aggregator
    agg = FeatureAggregator(
        entity_col='user_id',
        timestamp_col='transaction_date',
        value_col='amount'
    )
    
    # Calculate total spending over different windows
    print(f"\nCalculating features as of {observation_date}...")
    
    # Sum over 30 days
    sum_30d = agg.aggregate(transactions, '30D', 'sum', observation_date)
    print(f"\nTotal amount per user (30-day window):")
    print(sum_30d.head())
    
    # Mean over 90 days
    mean_90d = agg.aggregate(transactions, '90D', 'mean', observation_date)
    print(f"\nAverage amount per user (90-day window):")
    print(mean_90d.head())


def example_multiple_features():
    """Example 4: Generate multiple rolling features."""
    print("\n" + "=" * 60)
    print("Example 4: Multiple Rolling Features")
    print("=" * 60)
    
    transactions = create_sample_transaction_data()
    
    observation_date = pd.Timestamp('2023-06-30')
    
    agg = FeatureAggregator(
        entity_col='user_id',
        timestamp_col='transaction_date',
        value_col='amount'
    )
    
    # Generate multiple features at once
    print(f"\nGenerating multiple features as of {observation_date}...")
    features = agg.rolling_features(
        transactions,
        windows=['7D', '30D', '90D'],
        agg_funcs=['sum', 'mean', 'count'],
        observation_date=observation_date
    )
    
    print(f"\nGenerated features:")
    print(features.head())
    print(f"\nColumns: {list(features.columns)}")


def example_combined_workflow():
    """Example 5: Complete workflow with PIT and features."""
    print("\n" + "=" * 60)
    print("Example 5: Complete Point-in-Time Feature Engineering Workflow")
    print("=" * 60)
    
    transactions = create_sample_transaction_data()
    observation_date = '2023-06-30'
    
    # Step 1: Filter to historical data
    pit_builder = PointInTimeBuilder('user_id', 'transaction_date', observation_date)
    historical_data = pit_builder.transform(transactions)
    print(f"\n1. Historical data up to {observation_date}: {len(historical_data)} transactions")
    
    # Step 2: Create features
    agg = FeatureAggregator('user_id', 'transaction_date', 'amount')
    features = agg.rolling_features(
        historical_data,
        windows=['30D', '90D'],
        agg_funcs=['sum', 'mean', 'count'],
        observation_date=pd.Timestamp(observation_date)
    )
    print(f"2. Generated {len(features.columns)} feature columns")
    
    # Step 3: Get latest values
    latest = pit_builder.get_latest_values(historical_data, columns=['amount'])
    latest.rename(columns={'amount': 'last_transaction_amount'}, inplace=True)
    print(f"3. Added latest transaction amount for {len(latest)} users")
    
    # Step 4: Combine all features
    final_features = features.merge(latest, on='user_id', how='left')
    print(f"\n4. Final feature set:")
    print(final_features.head())


if __name__ == '__main__':
    example_basic_pit()
    example_latest_values()
    example_feature_aggregation()
    example_multiple_features()
    example_combined_workflow()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
