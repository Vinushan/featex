Feature Engineering with FeatEx
===============================

Feature engineering is the process of creating meaningful features from raw data that help
machine learning models make better predictions.

Time-Based Features
-------------------

Most business datasets have temporal aspects. FeatEx helps you build features that respect
the temporal ordering of your data.

Rolling Aggregations
~~~~~~~~~~~~~~~~~~~~

Create features by aggregating values over time windows:

.. code-block:: python

    from featex.features import FeatureAggregator

    transactions = pd.DataFrame({
        'customer_id': [1, 1, 1, 2, 2, 2],
        'date': pd.date_range('2023-01-01', periods=6, freq='D'),
        'amount': [100, 150, 200, 50, 75, 80]
    })

    agg = FeatureAggregator(
        entity_col='customer_id',
        timestamp_col='date',
        value_col='amount'
    )

    # Sum of transactions in last 7 days
    sum_7d = agg.aggregate(transactions, '7D', 'sum')

    # Average transaction amount in last 30 days
    mean_30d = agg.aggregate(transactions, '30D', 'mean')

Supported Aggregations
~~~~~~~~~~~~~~~~~~~~~~

- **sum** - Total value over the window
- **mean** - Average value
- **count** - Number of transactions
- **max** - Maximum value
- **min** - Minimum value
- **std** - Standard deviation
- **Custom functions** - Pass any callable

Multiple Features at Once
~~~~~~~~~~~~~~~~~~~~~~~~~

Generate many features efficiently:

.. code-block:: python

    # Create 6 features from 2 windows and 3 aggregations
    features = agg.rolling_features(
        transactions,
        windows=['7D', '30D'],
        agg_funcs=['sum', 'mean', 'count'],
        observation_date=pd.Timestamp('2023-02-01')
    )

    # Result has columns like:
    # - amount_sum_7D
    # - amount_mean_7D
    # - amount_count_7D
    # - amount_sum_30D
    # - amount_mean_30D
    # - amount_count_30D

Advanced Patterns
-----------------

Creating Target Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use PIT to create labels without leakage:

.. code-block:: python

    from featex.pit import PointInTimeBuilder

    # For each observation date, create a label from future data
    def create_label(customer_id, observation_date, lookahead_days=30):
        pit = PointInTimeBuilder(
            'customer_id', 'date', observation_date
        )

        future_pit = PointInTimeBuilder(
            'customer_id', 'date',
            observation_date + pd.Timedelta(days=lookahead_days)
        )

        # Get data in the lookahead window
        customer_data = transactions[
            transactions['customer_id'] == customer_id
        ]

        future_data = future_pit.transform(customer_data)
        historical_data = pit.transform(customer_data)

        # Label: did amount increase in the next 30 days?
        if len(future_data) > 0 and len(historical_data) > 0:
            future_total = future_data['amount'].sum()
            historical_total = historical_data['amount'].sum()
            return int(future_total > historical_total)
        return 0

Feature Normalization
~~~~~~~~~~~~~~~~~~~~~

Normalize features for better model performance:

.. code-block:: python

    from sklearn.preprocessing import StandardScaler

    # Standardize features
    scaler = StandardScaler()
    features_normalized = scaler.fit_transform(features.select_dtypes(float))

Handling Missing Data
~~~~~~~~~~~~~~~~~~~~~

Use the utility functions for missing data:

.. code-block:: python

    from featex.utils import fill_missing_entities

    # Fill missing values for entities without data at certain times
    complete_data = fill_missing_entities(
        transactions,
        entity_col='customer_id',
        timestamp_col='date',
        fill_value=0
    )

Feature Validation
------------------

Check data quality:

.. code-block:: python

    from featex.utils import get_data_quality_report

    report = get_data_quality_report(features)
    print(report['missing_value_pct'])
    print(report['memory_usage_mb'])

Best Practices
--------------

1. **Use consistent observation dates** across all features

2. **Document your feature definitions** - Save code that created each feature

3. **Handle edge cases** - Entities with insufficient history, inactive customers, etc.

4. **Monitor feature drift** - Check that feature distributions remain stable over time

5. **Validate temporal correctness** - Ensure no future data leakage

6. **Use appropriate window sizes** - Domain knowledge matters here:
   - E-commerce: hours to days
   - Financial services: days to weeks
   - Healthcare: weeks to months

Common Patterns
---------------

User Activity Features
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    agg = FeatureAggregator('user_id', 'event_date', 'value')

    activity_features = agg.rolling_features(
        events,
        windows=['1D', '7D', '30D'],
        agg_funcs=['count', 'sum'],
    )

Recency Features
~~~~~~~~~~~~~~~~

.. code-block:: python

    from featex.pit import PointInTimeBuilder

    pit = PointInTimeBuilder('user_id', 'event_date', observation_date)
    latest = pit.get_latest_values(events, columns=['value'])
    latest['days_since_last_event'] = (
        observation_date - latest['event_date']
    ).dt.days
