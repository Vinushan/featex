Quick Start
===========

Installation
------------

Install FeatEx from PyPI:

.. code-block:: bash

    uv pip install featex

Or install from source for development:

.. code-block:: bash

    git clone https://github.com/yourusername/featex.git
    cd featex
    uv pip install -e ".[dev]"

Basic Usage
-----------

Point-in-Time Dataset
~~~~~~~~~~~~~~~~~~~~~

Create a point-in-time snapshot of your data:

.. code-block:: python

    import pandas as pd
    from featex.pit import PointInTimeBuilder

    # Your data
    data = pd.DataFrame({
        'user_id': [1, 1, 2, 2],
        'timestamp': pd.date_range('2023-01-01', periods=4, freq='D'),
        'amount': [100, 150, 50, 75]
    })

    # Create point-in-time builder
    pit = PointInTimeBuilder(
        entity_col='user_id',
        timestamp_col='timestamp',
        observation_date='2023-01-02'
    )

    # Get historical data only
    historical_data = pit.transform(data)

Feature Aggregation
~~~~~~~~~~~~~~~~~~~

Aggregate features over time windows:

.. code-block:: python

    from featex.features import FeatureAggregator

    agg = FeatureAggregator(
        entity_col='user_id',
        timestamp_col='timestamp',
        value_col='amount'
    )

    # Calculate 7-day rolling sum
    features = agg.aggregate(data, '7D', 'sum')

Next Steps
----------

- Read the :doc:`guides/pit_datasets` guide for detailed PIT concepts
- Check out :doc:`guides/feature_engineering` for advanced features
- See the :doc:`api_reference` for complete API documentation
- Browse :ref:`examples` for more use cases
