import pandas as pd
from position_filters.filters import postal_code_filter, geo_filter
import os

# Read the txt data of the 4 files in the folder 'data'
df1 = pd.read_csv("data/raw_data/spipoll_1_200k_202311130947.txt", sep="\t")
df2 = pd.read_csv("data/raw_data/spipoll_200k_400k_202311130949.txt", sep="\t")
df3 = pd.read_csv("data/raw_data/spipoll_400k_200k_202311130959.txt", sep="\t")
df4 = pd.read_csv("data/raw_data/spipoll_600k_75k_202311131020.txt", sep="\t")

# Merge the 4 dataframes into one
df_spipoll = pd.concat([df1, df2, df3, df4])

# Separate the column "coordonnees_GPS" into 2 columns "latitude" and "longitude"
df_spipoll[["latitude", "longitude"]] = df_spipoll["coordonnees_GPS"].str.split(
    ", ", expand=True
).astype(float)
df_spipoll = df_spipoll.drop(columns=["coordonnees_GPS"])

# Remove variables that will never be used in the project
unused_vars = [
    "collection_nom",
    "user_pseudo",
    "user_email",
    "commentaire",
    "photo_lieu",
    "distance_ruche",
    "collection_heure_fin",
    "insecte_photo_1",
    "insecte_photo_2",
    "date_creation_bdd",
    "date_update_bdd",
]
df_spipoll = df_spipoll.drop(columns=unused_vars)


# Apply filters to get which data are in metropolitan France and which are not
df_poste = pd.read_csv("data/governmental_data/datagouv_codespostaux.csv", sep=";")
metropole_collections, non_metropole_collections = postal_code_filter(
    df_spipoll, df_poste
)
metropole_collections, non_metropole_collections = geo_filter(
    metropole_collections, non_metropole_collections
)

# Once the data are filtered, we can remove the rows
# that are not in metropolitan France
rows_to_remove = df_spipoll["collection_id"].isin(
    non_metropole_collections["collection_id"]
)
df_spipoll = df_spipoll[~rows_to_remove]

df_spipoll.to_csv("data/spipoll2.csv", index=False)

if __name__ == "__main__":
    # If the script is the one being executed, then the working directory is
    # the root of the project. Otherwise, it is the root of the package.
    if os.getcwd().endswith("data_treatment"):
        os.chdir("../../")
