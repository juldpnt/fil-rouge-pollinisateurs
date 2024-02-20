import pytest
import pandas as pd
from models.supervised.preprocessors import MetricsCalculatorNaive
from models.supervised.preprocessors import (
    HourToCos,
    DateToJulian,
    get_df_by_hours,
    get_df_by_months,
)


@pytest.fixture
def create_test_data():
    # Create test data for the transformer
    data = {
        "latitude": [0, 1, 2, 3, 3],
        "longitude": [0, 1, 2, 3, 0],
        "insecte_fr": ["A", "B", "C", "A", "A"],
        "collection_id": [1, 2, 1, 2, 3],
    }
    return pd.DataFrame(data)


def test_fit():
    # Test the fit method of MetricsCalculatorNaive
    calculator = MetricsCalculatorNaive(distance=1)
    X = create_test_data
    transformed_calculator = calculator.fit(X)
    assert transformed_calculator is calculator


def test_transform(create_test_data):
    # Test the transform method of MetricsCalculatorNaive
    calculator = MetricsCalculatorNaive(distance=1, clear_intermediate_steps=False)
    X = create_test_data
    transformed_data = calculator.transform(X)
    assert "specific_richness" in transformed_data.columns
    assert "density" in transformed_data.columns
    assert "collection_id_density" in transformed_data.columns
    assert "weighted_specific_richness" in transformed_data.columns


# test that the whole class works as intended with the test data
# in particular with the results of the transform method, i.e with fit_transform
def test_fit_transform(create_test_data):
    # Test the fit_transform method of MetricsCalculatorNaive
    calculator = MetricsCalculatorNaive(distance=1.5, clear_intermediate_steps=False)
    X = create_test_data
    transformed_data = calculator.fit_transform(X)
    assert transformed_data.iloc[-1]["specific_richness"] == 1
    assert transformed_data.iloc[-1]["density"] == 1
    assert transformed_data.iloc[-1]["collection_id_density"] == 1
    assert transformed_data.iloc[-1]["weighted_specific_richness"] == 1

    assert transformed_data.iloc[0]["density"] == 2
    assert transformed_data.iloc[2]["density"] == 3

    assert transformed_data.iloc[2]["collection_id_density"] == 2

    assert transformed_data.iloc[2]["weighted_specific_richness"] == 3 / 2


@pytest.mark.parametrize(
    "hour_input, expected_output",
    [(["2023-07-04 08:00:00", "2023-07-04 12:00:00"], [-0.5, -1.0])],
)
def test_hour_to_cos_transform(hour_input, expected_output):
    X = pd.DataFrame({"hour": hour_input})
    transformer = HourToCos("hour")
    transformed_X = transformer.fit_transform(X)
    assert transformed_X["hour_cos"].tolist() == pytest.approx(expected_output)


@pytest.mark.parametrize(
    "date_input",
    [("2023-10-12"), ("2023-07-04")],
)
def test_date_to_julian_transform(date_input):
    X = pd.DataFrame({"date": [date_input]})
    transformer = DateToJulian("date")
    transformed_X = transformer.fit_transform(X)
    assert "date_julian" in transformed_X.columns


def test_get_df_by_hours():
    df = pd.DataFrame({"time": ["2023-07-04 08:00:00", "2023-07-04 12:00:00", "2023-12-04 08:00:00"]})
    selected_df = get_df_by_hours(df, "time", [8])
    assert len(selected_df) == 2


def test_get_df_by_months():
    df = pd.DataFrame({"time": ["2023-07-04 08:00:00", "2023-10-12 12:00:00"]})
    selected_df = get_df_by_months(df, "time", [10])
    assert len(selected_df) == 1
