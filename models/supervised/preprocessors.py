"""
preprocessors.py

TODO: Add description
TODO: rassembler les calculs d'indices dans une fonction
"""

from tqdm import tqdm
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.spatial import KDTree
from sklearn.neighbors import BallTree


class MetricsCalculator(BaseEstimator, TransformerMixin):
    """
    A class for calculating metrics related to insect data.

    Parameters:
    - distance: float, the distance threshold for calculating metrics.
    - calculate_unique_insects: bool, whether to calculate the number of unique insects within the distance.
    - calculate_density: bool, whether to calculate the density of points within the distance.
    - compute_collection_id_density: bool, whether to calculate the density of collection IDs within the distance.
    """

    def __init__(
        self,
        distance,
        calculate_unique_insects=True,
        calculate_density=True,
        compute_collection_id_density=True,
    ):
        self.distance = distance
        self.calculate_unique_insects = calculate_unique_insects
        self.calculate_density = calculate_density
        self.compute_collection_id_density = compute_collection_id_density
        tqdm.pandas()

    def fit(self, X, y=None):
        """
        Fit the metrics calculator to the data.

        Parameters:
        - X: pandas DataFrame, the input data.

        Returns:
        - self: MetricsCalculator object.
        """
        self.tree = BallTree(X[["latitude", "longitude"]].values, metric='euclidean', leaf_size=1500)
        return self

    def transform(self, X):
        self.df = X
        coords = X[["latitude", "longitude"]].values
        print("ouf ?")
        indices_list = self.tree.query_radius(coords, self.distance)
        print("oui")
        metrics = []
        for indices in tqdm(indices_list):
            metrics.append(self._calculate_metrics(indices))

        metrics_df = pd.DataFrame(metrics)
        X = pd.concat([X, metrics_df], axis=1)

        return X

    def _calculate_metrics(self, indices):
        metrics = {}

        if self.calculate_unique_insects:
            metrics["specific_richness"] = self.df.iloc[indices]["insecte_fr"].nunique()

        if self.calculate_density:
            metrics["density"] = len(indices)

        if self.compute_collection_id_density:
            metrics["collection_id_density"] = self.df.iloc[indices]["collection_id"].nunique()

        if self.calculate_unique_insects and self.compute_collection_id_density:
            metrics["weighted_specific_richness"] = metrics["specific_richness"] / metrics["collection_id_density"]

        return metrics