"""
preprocessors.py

TODO: Add description
"""

from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from tqdm import tqdm

tqdm.pandas()


class MetricsCalculatorNaive(BaseEstimator, TransformerMixin):
    """
    Calculates metrics based on the provided distance value using a naive approach.

    The following metrics are calculated:

    * Specific richness: the number of unique insects
    * Density: the number of insects in a given area
    * Collection ID density: the number of unique collection IDs in a given area
    * Weighted specific richness: specific richness per collection ID density

    This is done by comparing the coordinates of each data point and finding all
    points that are within the specified distance.

    The transformer can be configured to calculate only the required metrics.
    """

    def __init__(
        self,
        distance: float,
        insect_col: str = "insecte_fr",
        collection_id_col: str = "collection_id",
        compute_unique_insects: bool = True,
        compute_density: bool = True,
        compute_weighted_specific_richness: bool = True,
        clear_intermediate_steps: bool = True,
    ) -> None:
        """
        Initializes a MetricsCalculatorNaive object.

        Args:
            distance (float): The distance value.
            insect_col (str, optional): The column name for the insect. Defaults to "insecte_fr".
            collection_id_col (str, optional): The column name for the collection ID. Defaults to "collection_id".
            compute_unique_insects (bool, optional): Whether to calculate unique insects. Defaults to True.
            compute_density (bool, optional): Whether to calculate density. Defaults to True.
            compute_weighted_specific_richness (bool, optional): Whether to compute collection ID density. Defaults to True.
            clear_intermediate_steps (bool, optional): Whether to clear the intermediate columns. Defaults to True.
        """
        self.distance = distance
        self.insect_col = insect_col
        self.collection_id_col = collection_id_col
        self.compute_unique_insects = compute_unique_insects
        self.compute_density = compute_density
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

    def transform(self, X: pd.DataFrame) -> "pd.DataFrame":
        """
        Transforms the input data by calculating metrics.

        Args:
            X (pandas.DataFrame): The input data.

        Returns:
            pandas.DataFrame: The transformed data with calculated metrics.
        """
        self.df = X
        print("Calculating metrics:\n--------------------\n")
        mask = X.progress_apply(self._get_mask, axis=1)
        metrics = mask.progress_apply(self._calculate_metrics)

        for key in metrics.iloc[0].keys():
            X.loc[:, key] = metrics.apply(lambda x: x[key])

        if self.clear_intermediate_steps:
            columns_to_drop = ["specific_richness", "density", "collection_id_density"]
            columns_to_drop = [col for col in columns_to_drop if col in X.columns]
            X = X.drop(columns=columns_to_drop)
        return X

    def _get_mask(self, row: pd.Series) -> "pd.Series":
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

        if self.compute_unique_insects or self.compute_weighted_specific_richness:
            insect_col_filtered = self.df.loc[mask, self.insect_col]
            metrics["specific_richness"] = insect_col_filtered.nunique()

        if self.compute_density:
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

    def transform(self, X: pd.DataFrame) -> "pd.DataFrame":
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

    def transform(self, X: pd.DataFrame) -> "pd.DataFrame":
        """
        Transform the input data by converting the date values to Julian days.

        Args:
            X (pd.DataFrame): The input data.

        Returns:
            pd.DataFrame: The transformed data with an additional column containing the Julian days.
        """
        new_col = self.date_col + "_julian"
        X[new_col] = pd.to_datetime(X[self.date_col], format="ISO8601").apply(
            lambda x: x.to_julian_date()
        )
        return X


def split_in_dummies(
    df: pd.DataFrame,
    column_name: str,
    sep: str = ",",
):
    """
    Split a column in dummy columns.
    """
    df_dummies = df[column_name].str.get_dummies(sep)
    df = pd.concat([df, df_dummies], axis=1)
    return df, list(df_dummies.columns)


def get_df_by_hours(
    df: pd.DataFrame,
    time_col: str,
    hours: List[int],
) -> "pd.DataFrame":
    """
    Select rows from a dataframe based on a list of hours.

    Args:
        df (pandas.DataFrame): The input dataframe.
        time_col (str): The name of the column containing the time values.
        hours (List[int]): A list of hours to select rows for.

    Returns:
        pandas.DataFrame: The selected dataframe.
    """
    X = df[time_col].copy()
    X = pd.to_datetime(X, format="ISO8601")
    return df[X.dt.hour.isin(hours)]


def get_df_by_months(
    df: pd.DataFrame, time_col: str, months: List[int]
) -> "pd.DataFrame":
    """
    Select rows from a dataframe based on a list of months.

    Args:
        df (pandas.DataFrame): The input dataframe.
        time_col (str): The name of the column containing the time values.
        months (List[int]): A list of months to select rows for.

    Returns:
        pandas.DataFrame: The selected dataframe.
    """
    X = df[time_col].copy()
    X = pd.to_datetime(X, format="ISO8601")
    return df[X.dt.month.isin(months)]


def random_sample_mask(
    df: pd.DataFrame,
    column_name: str,
    min_threshold: float,
    max_threshold: float,
    sample_percentage: float,
    random_state: int = 0,
) -> "pd.DataFrame":
    """
    Generate a random sample mask for filtering a DataFrame.

    Args:
        df (pandas.DataFrame): The input dataframe
        column_name (str): The name of the column to apply the mask
        min_threshold (float): The minimum threshold value for the mask
        max_threshold (float): The maximum threshold value for the mask
        sample_percentage (float): The percentage of the sample to be taken
        random_state (int, optional): The seed for the random number generator

    Returns:
        pandas.DataFrame: The filtered DataFrame based on the random sample mask
    """
    rng = np.random.default_rng(random_state)
    mask = (df[column_name] > min_threshold) & (df[column_name] < max_threshold)
    sample_indices = rng.choice(
        df[mask].index,
        size=int(np.count_nonzero(mask) * sample_percentage),
        replace=False,
    )
    mask[sample_indices] = False
    df_filtered = df[~mask]
    return df_filtered


class TrainTestUnderSampler:
    """
    TrainTestUnderSampler is a preprocessor that applies random under-sampling to the training data,
    and then splits the resulting dataset into training and testing sets.
    """

    def __init__(
        self,
        column_name: str,
        min_thresholds: List[float],
        max_thresholds: List[float],
        sample_percentages: List[float],
        random_state: int = 1,
    ) -> None:
        """
        Initializes the instance with the specified column name, minimum thresholds, maximum thresholds, sample percentages, and optional random state.

        Args:
            column_name (str): The name of the column.
            min_thresholds (List[float]): The list of minimum thresholds.
            max_thresholds (List[float]): The list of maximum thresholds.
            sample_percentages (List[float]): The list of sample percentages.
            random_state (int, optional): The random state for reproducibility. Default is 1.
        """
        self.column_name = column_name
        self.min_thresholds = min_thresholds
        self.max_thresholds = max_thresholds
        self.sample_percentages = sample_percentages
        self.random_state = random_state

    def preprocess(self, X, y):
        """
        Split the data into training and testing sets.
        Apply random sample mask with different thresholds and sample percentages.
        Returns the preprocessed training and testing data.

        Args:
            X (array-like): The input features.
            y (array-like): The target values.
        Returns:
            tuple: Preprocessed training and testing data (X_train, X_test, y_train, y_test).
        """
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state
        )

        # Apply random sample mask with different thresholds and sample percentages
        for min_thresh, max_thresh, sample_percentage in zip(
            self.min_thresholds, self.max_thresholds, self.sample_percentages
        ):
            X_temp = pd.concat([X_train, y_train], axis=1)
            X_temp = random_sample_mask(
                X_temp,
                self.column_name,
                min_thresh,
                max_thresh,
                sample_percentage,
                random_state=self.random_state,
            )
            X_train = X_temp.drop(columns=[self.column_name], axis=1)
            y_train = X_temp[self.column_name]

        return X_train, X_test, y_train, y_test
