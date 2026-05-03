Point-in-Time Datasets
======================

What is a Point-in-Time Dataset?
--------------------------------

A point-in-time (PIT) dataset is a snapshot of features and labels at a specific moment in time,
constructed using only information that was available at that moment. This is essential for
building machine learning models that:

1. **Avoid data leakage** - Don't use future data to predict the past
2. **Reflect realistic scenarios** - Models see the same data a practitioner would have seen
3. **Enable proper backtesting** - Validate model performance on truly historical predictions

Why Point-in-Time Matters
-------------------------

Imagine building a credit risk model. You want to predict whether a customer will default on a loan.

**Without Point-in-Time (Data Leakage):**

- Use all customer transactions to train the model
- Model learns patterns from transactions that happened AFTER the loan was made
- In production, you can't use this information (it hasn't happened yet!)
- Your model performs poorly on new data

**With Point-in-Time (Correct):**

- For each customer, use only transactions BEFORE the loan date
- Model learns patterns that would have been available at decision time
- In production, the model has access to the same information
- Your model generalizes much better

Example
-------

Let's build a PIT dataset for predicting customer churn:

.. code-block:: python

    import pandas as pd
    from featex.pit import PointInTimeBuilder
    from featex.features import FeatureAggregator

    # Transaction history
    transactions = pd.DataFrame({
        'customer_id': [1, 1, 1, 2, 2, 2],
        'date': pd.date_range('2023-01-01', periods=6, freq='D'),
        'amount': [100, 150, 200, 50, 75, 80]
    })

    # Churn labels (when customers churned)
    churn_labels = pd.DataFrame({
        'customer_id': [1, 2],
        'churn_date': pd.to_datetime(['2023-01-15', '2023-02-01']),
        'churned': [1, 1]
    })

    # For each churn event, create features from data BEFORE the churn date
    pit_datasets = []

    for _, row in churn_labels.iterrows():
        customer_id = row['customer_id']
        churn_date = row['churn_date']

        # Get transactions before churn
        pit = PointInTimeBuilder(
            entity_col='customer_id',
            timestamp_col='date',
            observation_date=churn_date
        )

        customer_data = transactions[transactions['customer_id'] == customer_id]
        historical = pit.transform(customer_data)

        # Aggregate features
        agg = FeatureAggregator(
            entity_col='customer_id',
            timestamp_col='date',
            value_col='amount'
        )

        features = agg.aggregate(
            historical,
            '30D',
            'sum',
            observation_date=churn_date
        )

        features['churned'] = row['churned']
        pit_datasets.append(features)

    # Combine all PIT datasets
    pit_dataset = pd.concat(pit_datasets, ignore_index=True)

This dataset now has the correct temporal structure for training and backtesting!

Best Practices
--------------

1. **Define clear observation dates** - Know exactly when you're making predictions

2. **Use consistent historical windows** - Use the same lookback periods for all entities

3. **Handle missing data carefully** - An entity with no history is different from an entity with zero value

4. **Validate temporal order** - Ensure feature timestamps are all before observation date

5. **Document your cutoffs** - Keep clear records of what data was used when

Common Pitfalls
---------------

❌ **Using data after the observation date**
   
   This leaks information from the future

✅ **Strictly filter data before observation date**

❌ **Different cutoff dates for different entities**
   
   Inconsistency causes training/serving mismatch

✅ **Use consistent observation dates across your dataset**

❌ **Forgetting to handle entities with no history**

✅ **Explicitly handle cases with insufficient data**
