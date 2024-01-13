import pandas as pd
from typing import Tuple


def postal_code_filter(
    df_spipoll, df_poste
) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    """
    Process the dataframes df_spipoll and df_poste to keep only the data of
    France.
    
    This should be used before the geo_filter function.

    Args:
        df_spipoll (pandas.DataFrame): The input dataframe which must contain
        columns "collection_id", "coordonnees_GPS", and "code_postal".
        df_poste (pandas.DataFrame): The input dataframe which must contain columns
        with postal codes of metropolitan France.

    Returns:
        tuple: A tuple containing two dataframes:
        df_filter_metropole and df_filter_hors_metropole
        which have to be used to filter df_spipoll.
    """
    df_filter = df_spipoll[["collection_id", "longitude", "latitude", "code_postal"]].copy()

    # Get rid of the postal codes of overseas territories
    df_poste = df_poste[["Code_postal"]].astype(str)
    df_poste = df_poste[~df_poste["Code_postal"].str.startswith(("97", "98"))]

    # Add a new column 'France metropolitaine' to df_spipoll with the data that are in df_poste
    df_filter["France metropolitaine"] = df_filter["code_postal"].isin(
        df_poste["Code_postal"]
    )
    # Keep only the first row for each collection_id
    df_filter = df_filter.drop_duplicates(subset="collection_id", keep="first")

    # Split df_filter into 2 dataframes whether the data are in metropolitan France or not
    df_filter_metropole = df_filter[df_filter["France metropolitaine"] == True]
    df_filter_hors_metropole = df_filter[df_filter["France metropolitaine"] == False]

    return df_filter_metropole, df_filter_hors_metropole


def geo_filter(df_spipoll_metropole, df_spipoll_hors_metropole):
    # northern-most, southern-most, western-most and eastern-most points of Metropolitan France
    latitude_nord = 51.065
    latitude_sud = 42.19
    longitude_ouest = -5.15
    longitude_est = 9.325

    # select the columns "collection_id", "longitude" and "latitude" from df_spipoll_metropole and df_spipoll_hors_metropole
    df_spipoll_metropole = df_spipoll_metropole[
        ["longitude", "latitude", "collection_id"]
    ].copy()
    df_spipoll_hors_metropole = df_spipoll_hors_metropole[
        ["longitude", "latitude", "collection_id"]
    ].copy()

    # rows from df_spipoll_metropole that are outside of Metropolitan France : false positives
    within_latitude_France_df = df_spipoll_metropole[
        (df_spipoll_metropole["latitude"] > latitude_sud)
        & (df_spipoll_metropole["latitude"] < latitude_nord)
    ]
    within_longitude_France_df = df_spipoll_metropole[
        (df_spipoll_metropole["longitude"] > longitude_ouest)
        & (df_spipoll_metropole["longitude"] < longitude_est)
    ]

    # identify the rows in df_spipoll_metropole that are both in within_latitude_France_df and within_longitude_France_df
    within_France_df = pd.merge(
        within_latitude_France_df,
        within_longitude_France_df,
        on=["collection_id", "longitude", "latitude"],
    )

    # add to df_spipoll_hors_metropole the rows that are in df_spipoll_metropole but not in within_France_df
    df_spipoll_hors_metropole = pd.concat(
        [
            df_spipoll_hors_metropole,
            df_spipoll_metropole[~df_spipoll_metropole.isin(within_France_df)].dropna(),
        ]
    )

    # remove from df_spipoll_metropole the rows that are not in within_France_df
    df_spipoll_metropole = df_spipoll_metropole[
        df_spipoll_metropole.isin(within_France_df)
    ].dropna()

    # rows from df_spipoll_hors_metropole that are inside of Metropolitan France : false negatives
    within_latitude_France_df = df_spipoll_hors_metropole[
        (df_spipoll_hors_metropole["latitude"] > latitude_sud)
        & (df_spipoll_hors_metropole["latitude"] < latitude_nord)
    ]
    within_longitude_France_df = df_spipoll_hors_metropole[
        (df_spipoll_hors_metropole["longitude"] > longitude_ouest)
        & (df_spipoll_hors_metropole["longitude"] < longitude_est)
    ]

    # identify the rows in df_spipoll_hors_metropole that are both in within_latitude_France_df and within_longitude_France_df
    within_France_df = pd.merge(
        within_latitude_France_df,
        within_longitude_France_df,
        on=["collection_id", "longitude", "latitude"],
    )

    # add to df_spipoll_metropole the rows that are in within_France_df
    df_spipoll_metropole = pd.concat(
        [
            df_spipoll_metropole,
            df_spipoll_hors_metropole[
                df_spipoll_hors_metropole.isin(within_France_df)
            ].dropna(),
        ]
    )

    # remove from df_spipoll_hors_metropole the rows that are in within_France_df
    df_spipoll_hors_metropole = df_spipoll_hors_metropole[
        ~df_spipoll_hors_metropole.isin(within_France_df)
    ].dropna()

    return df_spipoll_metropole, df_spipoll_hors_metropole
