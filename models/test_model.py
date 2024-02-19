from notebooks.utils import setup_env_path
import pandas as pd

# setup_env_path()
path = "data/temporary_data/spipoll.csv"
data = pd.read_csv(path)
restricted_vars = [
    "collection_id",
#    "plante_sc",
#    "plante_fr",
#    "insecte_sc",
    "insecte_fr",
#    "temperature",
#    "vent",
    "latitude",
    "longitude",
#    "nebulosite",
#    "collection_heure_debut", 
]
df = data[restricted_vars].copy()

df = data[restricted_vars].copy().sample(frac=0.1, random_state=1)
df.shape

from models.supervised.preprocessors import MetricsCalculatorNaive
distance = 0.5

calculator = MetricsCalculatorNaive(distance=distance)
calculator.fit(df)

df_transformed = calculator.transform(df)

import sys

print(df_transformed.columns)
print(sys.getsizeof(df_transformed))
print(sys.getsizeof(df))