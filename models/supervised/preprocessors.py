"""
preprocessors.py

TODO: Add description
TODO: rassembler les calculs d'indices dans une fonction
"""

from typing import List, Dict
from tqdm import tqdm
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.spatial import KDTree
from sklearn.neighbors import BallTree


class MetricsCalculatorTree(BaseEstimator, TransformerMixin):
    """
    A class for calculating metrics related to insect data using a tree-based approach.
    It is not memory-efficient but is way faster than the naive approach.

    TODO: Compress the data to reduce memory usage by grouping the data by collection_id and
    then joining the results back to the original dataframe.
    Or use a more memory-efficient data structure, with a divide-and-conquer approach (chunking the data).
    """

    def __init__(
        self,
        distance: float,
        calculate_unique_insects: bool = True,
        calculate_density: bool = True,
        compute_collection_id_density: bool = True,
    ) -> None:
        """
        Initializes a Preprocessor object.

        Args:
            distance (float): The distance value.
            calculate_unique_insects (bool, optional): Whether to calculate unique insects. Defaults to True.
            calculate_density (bool, optional): Whether to calculate density. Defaults to True.
            compute_collection_id_density (bool, optional): Whether to compute collection ID density. Defaults to True.
        """
        self.distance = distance
        self.calculate_unique_insects = calculate_unique_insects
        self.calculate_density = calculate_density
        self.compute_collection_id_density = compute_collection_id_density
        tqdm.pandas()

    def fit(self, X: pd.DataFrame, y=None) -> "MetricsCalculatorTree":
        """
        Fit the metrics calculator to the data.

        Args:
            X (pandas.DataFrame): The input data.
            y (optional): The target data (default: None).

        Returns:
            self (MetricsCalculator): The fitted MetricsCalculator object.
        """
        self.tree = BallTree(
            X[["latitude", "longitude"]].values, metric="euclidean", leaf_size=1500
        )
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input data by calculating metrics.

        Args:
            X (pandas.DataFrame): The input data.

        Returns:
            pandas.DataFrame: The transformed data with calculated metrics.
        """
        self.df = X
        coords = X[["latitude", "longitude"]].values
        indices_list = self.tree.query_radius(coords, self.distance)
        metrics = []
        for indices in tqdm(indices_list):
            metrics.append(self._calculate_metrics(indices))

        metrics_df = pd.DataFrame(metrics)
        X = pd.concat([X, metrics_df], axis=1)

        return X

    def _calculate_metrics(self, indices: List[int]) -> Dict[str, float]:
        """
        Calculate metrics based on the given indices.

        Args:
            indices (list): The indices of data points within the distance.

        Returns:
            dict: The calculated metrics.
        """
        metrics = {}

        if self.calculate_unique_insects:
            metrics["specific_richness"] = self.df.iloc[indices]["insecte_fr"].nunique()

        if self.calculate_density:
            metrics["density"] = len(indices)

        if self.compute_collection_id_density:
            metrics["collection_id_density"] = self.df.iloc[indices][
                "collection_id"
            ].nunique()

        if self.calculate_unique_insects and self.compute_collection_id_density:
            metrics["weighted_specific_richness"] = (
                metrics["specific_richness"] / metrics["collection_id_density"]
            )

        return metrics


class MetricsCalculatorNaive(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        distance: float,
        calculate_unique_insects: bool = True,
        calculate_density: bool = True,
        compute_collection_id_density: bool = True,
    ) -> None:
        """
        Initializes a MetricsCalculatorNaive object.

        Args:
            distance (float): The distance value.
            calculate_unique_insects (bool, optional): Whether to calculate unique insects. Defaults to True.
            calculate_density (bool, optional): Whether to calculate density. Defaults to True.
            compute_collection_id_density (bool, optional): Whether to compute collection ID density. Defaults to True.
        """
        self.distance = distance
        self.calculate_unique_insects = calculate_unique_insects
        self.calculate_density = calculate_density
        self.compute_collection_id_density = compute_collection_id_density
        tqdm.pandas()

    def fit(self, X: pd.DataFrame, y=None) -> "MetricsCalculatorNaive":
        """Fit the transformer. This is a placeholder method as this transformer doesn't need to be fitted.

        Args:
            X (DataFrame): The input data.
            y (Series, optional): The target data. Defaults to None.

        Returns:
            self
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input data by calculating metrics.

        Args:
            X (pandas.DataFrame): The input data.

        Returns:
            pandas.DataFrame: The transformed data with calculated metrics.
        """
        self.df = X

        metrics = []
        for _, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            mask = self._get_mask(row)
            metrics.append(self._calculate_metrics(mask))

        metrics_df = pd.DataFrame(metrics)
        X = pd.concat([X, metrics_df], axis=1)

        return X

    def _get_mask(self, row: pd.Series) -> pd.Series:
        """
        Returns a boolean mask with rows within the specified distance.

        Args:
            row (pandas.Series): The row to compare distances with.

        Returns:
            pandas.Series: A boolean mask indicating which rows are within the specified distance.
        """
        lat_diff = np.abs(self.df["latitude"] - row["latitude"])
        lon_diff = np.abs(self.df["longitude"] - row["longitude"])
        mask = (lat_diff < self.distance) & (lon_diff < self.distance)
        return mask

    def _calculate_metrics(self, mask: pd.Series) -> Dict[str, float]:
        """
        Calculate metrics based on the given indices.

        Args:
            indices (list): The indices of data points within the distance.

        Returns:
            dict: The calculated metrics.
        """
        metrics = {}

        if self.calculate_unique_insects:
            metrics["specific_richness"] = self.df[mask]["insecte_fr"].nunique()

        if self.calculate_density:
            metrics["density"] = mask.sum()

        if self.compute_collection_id_density:
            metrics["collection_id_density"] = self.df[mask]["collection_id"].nunique()

        if self.calculate_unique_insects and self.compute_collection_id_density:
            metrics["weighted_specific_richness"] = (
                metrics["specific_richness"] / metrics["collection_id_density"]
            )

        return metrics
