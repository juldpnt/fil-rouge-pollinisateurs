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

tqdm.pandas()

class MetricsCalculatorNaive(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        distance: float,
        insect_col: str = "insecte_fr",
        collection_id_col: str = "collection_id",
        calculate_unique_insects: bool = True,
        calculate_density: bool = True,
        compute_weighted_specific_richness: bool = True,
        clear_intermediate_steps: bool = True,
    ) -> None:
        """
        Initializes a MetricsCalculatorNaive object.

        Args:
            distance (float): The distance value.
            insect_col (str, optional): The column name for the insect. Defaults to "insecte_fr".
            collection_id_col (str, optional): The column name for the collection ID. Defaults to "collection_id".
            calculate_unique_insects (bool, optional): Whether to calculate unique insects. Defaults to True.
            calculate_density (bool, optional): Whether to calculate density. Defaults to True.
            compute_weighted_specific_richness (bool, optional): Whether to compute collection ID density. Defaults to True.
            clear_intermediate_steps (bool, optional): Whether to clear the intermediate columns. Defaults to True.
        """
        self.distance = distance
        self.insect_col = insect_col
        self.collection_id_col = collection_id_col
        self.calculate_unique_insects = calculate_unique_insects
        self.calculate_density = calculate_density
        self.compute_weighted_specific_richness = compute_weighted_specific_richness
        self.clear_intermediate_steps = clear_intermediate_steps

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
        mask = X.progress_apply(self._get_mask, axis=1)
        metrics = mask.progress_apply(self._calculate_metrics)
        for key in metrics.iloc[0].keys():
            X[key] = metrics.apply(lambda x: x[key])
        if self.clear_intermediate_steps:
            X = X.drop(columns=["specific_richness", "density", "collection_id_density"])
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
            mask (pd.Series): Boolean mask for filtering data points.

        Returns:
            dict: The calculated metrics.
        """
        metrics = {}

        if self.calculate_unique_insects or self.compute_weighted_specific_richness:
            insect_col_filtered = self.df.loc[mask, self.insect_col]
            metrics["specific_richness"] = insect_col_filtered.nunique()

        if self.calculate_density:
            metrics["density"] = mask.sum()

        if self.compute_weighted_specific_richness:
            collection_id_col_filtered = self.df.loc[mask, self.collection_id_col]
            metrics["collection_id_density"] = collection_id_col_filtered.nunique()
            metrics["weighted_specific_richness"] = (
                metrics["specific_richness"] / metrics["collection_id_density"]
            )

        return metrics


class HourToCos(BaseEstimator, TransformerMixin):
    def __init__(self, hour_col: str) -> None:
        """
        Initialize the HourToCos transformer.

        Args:
            hour_col (str): The name of the column containing the time values.

        Returns:
            None
        """
        self.hour_col = hour_col

    def fit(self, X: pd.DataFrame, y=None) -> "HourToCos":
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

        new_col = self.hour_col + "_cos"
        X[new_col] = pd.to_datetime(X[self.hour_col])
        X[new_col] = X[new_col].dt.hour + X[new_col].dt.minute / 60
        X[new_col] = X[new_col] * 2 * np.pi / 24
        X[new_col] = X[new_col].apply(np.cos)
        return X

class DateToJulian(BaseEstimator, TransformerMixin):
    def __init__(self, date_col: str) -> None:
        """
        Initialize the DateToJulian transformer.

        Args:
            date_col (str): The name of the column containing the date values.

        Returns:
            None
        """
        self.date_col = date_col

    def fit(self, X: pd.DataFrame, y=None) -> "DateToJulian":
        """
        Fit the transformer to the data.

        Args:
            X (pd.DataFrame): The input data.
            y: Ignored.

        Returns:
            self (DateToJulian): The fitted transformer.
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input data by converting the date values to Julian days.

        Args:
            X (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: The transformed data with an additional column containing the Julian days.
        """
        new_col = self.date_col + "_julian"
        X[new_col] = pd.to_datetime(X[self.date_col]).apply(lambda x: x.to_julian_date())
        return X
    
def get_df_by_hours(df: pd.DataFrame, time_col: str, hours: List[int], ) -> pd.DataFrame:
    """
    Select rows from a dataframe based on a list of hours.

    Args:
        df (pandas.DataFrame): The input dataframe.
        time_col (str): The name of the column containing the time values.
        hours (List[int]): A list of hours to select rows for.

    Returns:
        pandas.DataFrame: The selected dataframe.
    """
    X = df["collection_heure_debut"].copy()
    X = pd.to_datetime(X)
    return df[X.dt.hour.isin(hours)]