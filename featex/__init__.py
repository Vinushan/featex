"""
FeatEx - Feature Engineering for Point-in-Time Datasets

A Python library for building historically accurate, point-in-time datasets
for machine learning without data leakage.
"""

__version__ = "0.1.0"
__author__ = "FeatEx Contributors"
__license__ = "MIT"

from featex.pit import PointInTimeBuilder
from featex.features import FeatureAggregator

__all__ = [
    "PointInTimeBuilder",
    "FeatureAggregator",
]
