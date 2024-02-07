"""
preprocessors.py

TODO: Add description
TODO: rassembler les calculs d'indices dans une fonction
"""

from tqdm import tqdm
import numpy as np

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
        self.tree = BallTree(X[["latitude", "longitude"]].values, metric='euclidean')
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
        X["_temp_indices"] = X.progress_apply(self._get_neighbours, axis=1)

        if self.calculate_unique_insects:
            print("Calculating unique insects...")
            X = self.get_specific_richness(X)

        if self.calculate_density:
            print("Calculating density...")
            X = self.get_density(X)

        if self.compute_collection_id_density:
            print("Calculating collection id density...")
            X = self.get_collection_id_density(X)

            print("Calculating weighted specific richness...")
            X = self.get_weighted_specific_richness(X)

        print("Done! \n")
        X = X.drop(columns=["_temp_indices"])

        return X

    def _get_neighbours(self, X):
        """
        Get the indices of the neighbours within the distance for the input data.

        Parameters:
        - X: pandas DataFrame, the input data.

        Returns:
        - list of lists, the indices of the neighbours within the distance for each row.
        """
        coords = X[["latitude", "longitude"]].values.reshape(1, -1)
        indices = self.tree.query_radius(coords, self.distance)
        indices = np.concatenate(indices)
        return indices

    def get_specific_richness(self, X):
        X["specific_richness"] = X["_temp_indices"].progress_apply(
            lambda indices: self.df.iloc[indices]["insecte_fr"].nunique()
        )
        return X

    def get_density(self, X):
        X["density"] = X["_temp_indices"].progress_apply(len)
        return X

    def get_collection_id_density(self, X):
        X["collection_id_density"] = X["_temp_indices"].progress_apply(
            lambda indices: self.df.iloc[indices]["collection_id"].nunique()
        )
        return X

    def get_weighted_specific_richness(self, X):
        X["weighted_specific_richness"] = X["specific_richness"] / X["collection_id_density"]
        return X