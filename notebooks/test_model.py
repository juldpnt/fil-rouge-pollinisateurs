from utils import setup_env_path
import pandas as pd

setup_env_path()
path = "data/temporary_data/spipoll.csv"
data = pd.read_csv(path)
restricted_vars = [
    "collection_id",
    "plante_sc",
    "plante_fr",
    "insecte_sc",
    "insecte_fr",
    "temperature",
    "vent",
    "latitude",
    "longitude",
    "nebulosite",
    "collection_heure_debut"
]
df = data[restricted_vars].copy()

df = data[restricted_vars].copy().sample(frac=0.1, random_state=1)
df.shape

from models.supervised.preprocessors import MetricsCalculator

distance = 0.5

calculator = MetricsCalculator(distance=distance)
calculator.fit(df)

df_transformed = calculator.transform(df)