"""
preprocessors.py

TODO: Add description
TODO: rassembler les calculs d'indices dans une fonction
"""

from enum import verify
from tqdm import tqdm
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.spatial import KDTree


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
        self.tree = KDTree(X[["latitude", "longitude"]].values)
        return self

    def transform(self, X):
        """
        Transform the input data by calculating metrics.

        Parameters:
        - X: pandas DataFrame, the input data.

        Returns:
        - X: pandas DataFrame, the transformed data with calculated metrics.
        """
        self.df = X
        
        if self.calculate_unique_insects:
            print("Calculating unique insects...")
            X["specific_richness"] = X.progress_apply(
                self._calculate_unique_insects, axis=1
            )

        if self.calculate_density:
            print("Calculating density...")
            X["density"] = X.progress_apply(self._calculate_density, axis=1)

        if self.compute_collection_id_density:
            print("Calculating collection id density...")
            X["collection_id_density"] = X.progress_apply(
                self._compute_collection_id_density, axis=1
            )
            print("Calculating weighted specific richness...")
            X["weighted_specific_richness"] = (
                X["specific_richness"] / X["collection_id_density"]
            )
        return X

    def _calculate_unique_insects(self, row):
        """
        Calculate the number of unique insects within the distance for a given row.

        Parameters:
        - row: pandas Series, a row of the input data.

        Returns:
        - int, the number of unique insects within the distance.
        """
        indices = self.tree.query_ball_point(
            [row["latitude"], row["longitude"]], self.distance
        )
        return self.df.iloc[indices]["insecte_fr"].nunique()

    def _calculate_density(self, row):
        """
        Calculate the density of points within the distance for a given row.

        Parameters:
        - row: pandas Series, a row of the input data.

        Returns:
        - int, the density of points within the distance.
        """
        # TODO: use the KDTree to calculate the density
        lat = row["latitude"]
        lon = row["longitude"]
        return self.df[
            (np.abs(self.df["latitude"] - lat) <= self.distance)
            & (np.abs(self.df["longitude"] - lon) <= self.distance)
        ].shape[0]

    def _compute_collection_id_density(self, row):
        """
        Calculate the density of collection IDs within the distance for a given row.

        Parameters:
        - row: pandas Series, a row of the input data.

        Returns:
        - int, the density of collection IDs within the distance.
        """
        # TODO: use the KDTree to calculate the density
        lat = row["latitude"]
        lon = row["longitude"]
        return self.df[
            (np.abs(self.df["latitude"] - lat) <= self.distance)
            & (np.abs(self.df["longitude"] - lon) <= self.distance)
        ]["collection_id"].nunique()
