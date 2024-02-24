import pandas as pd
from models.preprocessors import TrainTestUnderSampler
from models.supervised.workflow import (
    preprocess_data,
    train_pipe,
)

use_backup = False


def main():
    path = "data/raw_data/spipoll.csv"
    data = pd.read_csv(path).sample(frac=0.05, random_state=1).copy()

    hour_range = [i for i in range(0, 24)]
    month_range = [i for i in range(1, 13)]

    distance = 0.5

    if use_backup:
        df_transformed = pd.read_csv("models/supervised/df_transformed.csv")
    else:
        df_transformed, dummies_col = preprocess_data(
            data,
            distance,
            hour_range,
            month_range,
            "habitat",
            "insecte_ordre",
        )

    numeric_features = [
        # "latitude",
        # "longitude",
        "collection_heure_debut_cos",
        "collection_heure_debut_julian",
    ]

    ordinal_features = ["vent", "nebulosite", "temperature"]

    nominal_features = [
        "plante_famille",
        "insecte_ordre",
    ] + dummies_col

    y_column_name = "specific_richness"

    kwargs_sampler = {
        "min_thresholds": [0.0],
        "max_thresholds": [0.0],
        "sample_percentages": [0.5],
        "column_name": "specific_richness",
    }

    sampler = TrainTestUnderSampler(**kwargs_sampler)
    pipe, X_test, y_test = train_pipe(
        df_transformed,
        numeric_features,
        ordinal_features + nominal_features,
        ordinal_features,
        nominal_features,
        y_column_name,
        sampler,
    )

    pipe.get_metrics(X_test, y_test)

    return pipe
