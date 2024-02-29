import pandas as pd
from models.preprocessors import TrainTestUnderSampler
from models.supervised.workflow import (
    preprocess_data,
    train_pipe,
)
from models.preprocessors import get_df_by_hours, get_df_by_months

### SETUP: PARAMETER TO CHANGE
# If you already have a preprocessed dataset with the target computed
# Please check preprocess_data function to check what must be in the file.
use_backup = True

# NOT USABLE IN THIS STATE
def main():
    ## PARAMETERS
    path = "data/raw_data/spipoll.csv"
    path_backup = "spipoll_target_medium.csv"
    hour_range = [i for i in range(0, 24)]
    month_range = [i for i in range(1, 13)]

    target_source = "insecte_ordre"
    dummy_col = "habitat"
    distance = 0.5
    y_column_name = "specific_richness"
    
    
    if use_backup:
        df_transformed = pd.read_csv(path_backup)

    else:
        data = pd.read_csv(path).sample(frac=0.05, random_state=1).copy()
        df_transformed, dummies_col = preprocess_data(
            data,
            distance,
            hour_range,
            month_range,
            dummy_col,
            target_source,
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
        target_source,
    ] + dummies_col

    

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
