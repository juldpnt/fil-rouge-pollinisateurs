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
from sklearn.neighbors import BallTree

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
        print("Calculating metrics...")
        for i, row in tqdm(X.iterrows(), total=X.shape[0]):
            mask = self._get_mask(row)
            metric = self._calculate_metrics(mask)
            for key, value in metric.items():
                X.loc[i, key] = value

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

class MetricsCalculatorTree(BaseEstimator, TransformerMixin):
    """
    A class for calculating metrics related to insect data. Not recommended for large datasets but is faster than the naive.

    Parameters:
    - distance: float, the distance threshold for calculating metrics.
    - calculate_unique_insects: bool, whether to calculate the number of unique insects within the distance.
    - calculate_density: bool, whether to calculate the density of points within the distance.
    - compute_collection_id_density: bool, whether to calculate the density of collection IDs within the distance.
    
    TODO:
    - change docstring to google format
    - optimize by doing divide and conquer strategy (maybe ?) by splitting the data into smaller chunks
    eventhough it might remove certain insects from the calculation
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
    
class HourToCos(BaseEstimator, TransformerMixin):
    def __init__(self, time_col: str) -> None:
        """
        Initialize the HourToCos transformer.

        Args:
            time_col (str): The name of the column containing the time values.

        Returns:
            None
        """
        self.time_col = time_col
        
    def fit(self, X: pd.DataFrame, y=None) -> "TimeToCos":
        """
        Fit the transformer to the data.

        Args:
            X (pd.DataFrame): The input data.
            y: Ignored.

        Returns:
            self (TimeToCos): The fitted transformer.
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input data by converting the time values to cosine values.

        Args:
            X (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: The transformed data with an additional column containing the cosine values.
        """
        
        new_col = self.time_col + "_cos"
        X[new_col] = pd.to_datetime(X[self.time_col])
        X[new_col] = X[new_col].dt.hour + X[new_col].dt.minute / 60
        X[new_col] = X[new_col] * 2 * np.pi / 24
        X[new_col] = X[new_col].apply(np.cos)
        return X