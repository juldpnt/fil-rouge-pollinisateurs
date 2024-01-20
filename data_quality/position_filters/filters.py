import pandas as pd
from typing import Tuple


def postal_code_filter(
    df_spipoll: "pd.DataFrame", df_poste: "pd.DataFrame", save=False
) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    """
    Filters the given dataframes based on postal code to later only
    include the data within Metropolitan France.

    This should be used before the geo_filter function.

    Args:
        df_spipoll (pandas.DataFrame): The input dataframe which must contain
        columns "collection_id", "coordonnees_GPS", and "code_postal".
        df_poste (pandas.DataFrame): The input dataframe which must contain
        columns with postal codes of metropolitan France.
        save (bool): If True, the dataframes df_filter_metropole and
        df_filter_hors_metropole are saved in the folder data/temporary_data.

    Returns:
        tuple: A tuple containing two dataframes:
        df_filter_metropole and df_filter_hors_metropole
        which have to be used to filter df_spipoll.
    """
    df_filter = df_spipoll[
        ["collection_id", "longitude", "latitude", "code_postal"]
    ].copy()

    # Get rid of the postal codes of overseas territories
    df_poste = df_poste[["Code_postal"]].astype(str)
    df_poste = df_poste[~df_poste["Code_postal"].str.startswith(("97", "98"))]

    # Add a new column 'France metropolitaine' to df_spipoll with the data
    # that are in df_poste
    df_filter["France metropolitaine"] = df_filter["code_postal"].isin(
        df_poste["Code_postal"]
    )
    # Keep only the first row for each collection_id
    df_filter = df_filter.drop_duplicates(subset="collection_id", keep="first")

    # Split df_filter into 2 dataframes whether the data are in metropolitan
    # France or not
    df_filter_metropole = df_filter[df_filter["France metropolitaine"]]
    df_filter_hors_metropole = df_filter[df_filter["France metropolitaine"] == False]

    if save:
        df_filter_metropole.to_csv(
            "data/temporary_data/spipoll_metropole.csv", index=False
        )
        df_filter_hors_metropole.to_csv(
            "data/temporary_data/spipoll_hors_metropole.csv", index=False
        )

    return df_filter_metropole, df_filter_hors_metropole


def geo_filter(
    df_spipoll_metropole, df_spipoll_hors_metropole, save=False
) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    """
    Filters the given dataframes based on geographic coordinates to include
    only the data within Metropolitan France.

    Args:
        df_spipoll_metropole (DataFrame): DataFrame containing data within
        Metropolitan France.
        df_spipoll_hors_metropole (DataFrame): DataFrame containing data
        outside of Metropolitan France.
        save (bool, optional): Flag indicating whether to save the filtered
        dataframes to CSV files. Defaults to False.

    Returns:
        Tuple[DataFrame, DataFrame]: A tuple containing the filtered DataFrame
        for Metropolitan France and the filtered DataFrame for outside of
        Metropolitan France.
    """
    # Northern-most, southern-most, western-most and eastern-most points of
    # Metropolitan France
    latitude_nord = 51.065
    latitude_sud = 42.19
    longitude_ouest = -5.15
    longitude_est = 9.325

    # Select the columns "collection_id", "longitude" and "latitude" from
    # df_spipoll_metropole and df_spipoll_hors_metropole
    df_spipoll_metropole = df_spipoll_metropole[
        ["longitude", "latitude", "collection_id"]
    ].copy()
    df_spipoll_hors_metropole = df_spipoll_hors_metropole[
        ["longitude", "latitude", "collection_id"]
    ].copy()

    # Rows from df_spipoll_metropole that are outside of Metropolitan France :
    # false positives
    within_latitude_France_df = df_spipoll_metropole[
        (df_spipoll_metropole["latitude"] > latitude_sud)
        & (df_spipoll_metropole["latitude"] < latitude_nord)
    ]
    within_longitude_France_df = df_spipoll_metropole[
        (df_spipoll_metropole["longitude"] > longitude_ouest)
        & (df_spipoll_metropole["longitude"] < longitude_est)
    ]

    # Identify the rows in df_spipoll_metropole that are both in
    # within_latitude_France_df and within_longitude_France_df
    df_spipoll_hors_metropole.reset_index(drop=True, inplace=True)
    within_France_df = within_latitude_France_df[
        within_latitude_France_df["collection_id"].isin(
            within_longitude_France_df["collection_id"]
        )
    ]

    # Add to df_spipoll_hors_metropole the rows that are in
    # df_spipoll_metropole but not in within_France_df
    df_spipoll_hors_metropole = pd.concat(
        [
            df_spipoll_hors_metropole,
            df_spipoll_metropole[~df_spipoll_metropole.isin(within_France_df)].dropna(),
        ]
    )

    # Remove from df_spipoll_metropole the rows that are not in
    # within_France_df
    df_spipoll_metropole = df_spipoll_metropole[
        df_spipoll_metropole.isin(within_France_df)
    ].dropna()

    # Rows from df_spipoll_hors_metropole that are inside of Metropolitan
    # France : false negatives
    within_latitude_France_df = df_spipoll_hors_metropole[
        (df_spipoll_hors_metropole["latitude"] > latitude_sud)
        & (df_spipoll_hors_metropole["latitude"] < latitude_nord)
    ]
    within_longitude_France_df = df_spipoll_hors_metropole[
        (df_spipoll_hors_metropole["longitude"] > longitude_ouest)
        & (df_spipoll_hors_metropole["longitude"] < longitude_est)
    ]

    # Identify the rows in df_spipoll_hors_metropole that are both in
    # within_latitude_France_df and within_longitude_France_df
    within_France_df = within_latitude_France_df[
        within_latitude_France_df["collection_id"].isin(
            within_longitude_France_df["collection_id"]
        )
    ]

    # Add to df_spipoll_metropole the rows that are in within_France_df
    df_spipoll_metropole = pd.concat(
        [
            df_spipoll_metropole,
            df_spipoll_hors_metropole[
                df_spipoll_hors_metropole.isin(within_France_df)
            ].dropna(),
        ]
    )

    # Remove from df_spipoll_hors_metropole the rows that are in
    # within_France_df
    df_spipoll_hors_metropole = df_spipoll_hors_metropole[
        ~df_spipoll_hors_metropole.isin(within_France_df)
    ].dropna()
    if save:
        df_spipoll_metropole.to_csv(
            "data/temporary_data/spipoll_metropole.csv", index=False
        )
        df_spipoll_hors_metropole.to_csv(
            "data/temporary_data/spipoll_hors_metropole.csv", index=False
        )
    return df_spipoll_metropole, df_spipoll_hors_metropole
