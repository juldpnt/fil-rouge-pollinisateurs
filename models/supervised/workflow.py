import matplotlib.pyplot as plt
import pandas as pd


from typing import List, Tuple

from models.preprocessors import DateToJulian, HourToCos
from models.preprocessors import MetricsCalculatorNaive as MetricsCalculator
from models.preprocessors import (
    get_df_by_hours,
    get_df_by_months,
    split_in_dummies,
)
from models.supervised.pipeline import CustomPipeline


def preprocess_data(
    data: pd.DataFrame,
    distance: float,
    hour_range: List[int],
    month_range: List[int],
    col_to_dummy: str,
    insect_col: str,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Preprocess the input data by selecting by hour and month, transforming temporal features
    to numeric,
    splitting into dummies, computing metrics target, and returning the preprocessed data
    and listof dummy column names.

    Args:
        data (pd.DataFrame): The input data to be preprocessed.
        distance (float): The distance value for metrics calculation.
        hour_range (List[int]): The range of hours to select in the data.
        month_range (List[int]): The range of months to select in the data.
        col_to_dummy (str): The name of the column to split into dummies.
        insect_col (str): The name of the column representing insects.

    Returns:
        Tuple[pd.DataFrame, List[str]]: The preprocessed data and the list of dummy column names.
    """
    print("\nPreprocessing data:\n--------------------\n")
    # Select data by hour and month
    data = get_df_by_hours(data, "collection_heure_debut", hour_range)
    data = get_df_by_months(data, "collection_heure_debut", month_range)

    # Temporal features transformation to numeric
    data = HourToCos(hour_col="collection_heure_debut").fit_transform(data)
    data = DateToJulian(date_col="collection_heure_debut").fit_transform(data)

    data, dummies_col = split_in_dummies(data, col_to_dummy)

    # Compute metrics target
    calculator = MetricsCalculator(
        distance=distance, clear_intermediate_steps=False, insect_col=insect_col
    )
    calculator.fit(data)
    data = calculator.transform(data)

    return data, dummies_col


def get_training_data(df_transformed, used_features, sampler, y_column_name):
    """
    Return training and testing data after preprocessing, given the transformed dataframe,
    used features, sampler, and target column name.
    """
    X = df_transformed[used_features]
    y = df_transformed[y_column_name]

    X_train, X_test, y_train, y_test = sampler.preprocess(X, y)

    return X_train, X_test, y_train, y_test


def train_pipe(
    df_transformed,
    numeric_features,
    categorical_features,
    ordinal_features,
    nominal_features,
    y_column_name,
    sampler,
):
    """
    Train the pipeline with the given transformed dataframe and features, 
    and return the trained pipeline, test features, and test labels.

    Args:
        df_transformed: Transformed dataframe
        numeric_features: List of numeric features
        categorical_features: List of categorical features
        ordinal_features: List of ordinal features
        nominal_features: List of nominal features
        y_column_name: Name of the target column
        sampler: Sampler for handling imbalanced data

    Returns:
        Trained pipeline, test features, and test labels
    """
    print("\nTraining pipeline:\n--------------------\n")
    X_train, X_test, y_train, y_test = get_training_data(
        df_transformed, numeric_features + categorical_features, sampler, y_column_name
    )
    pipe = CustomPipeline(
        numeric_features, categorical_features, ordinal_features, nominal_features
    )

    pipe.fit(X_train, y_train)

    return pipe, X_test, y_test
