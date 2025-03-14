import pandas as pd
import constants as c
from utils import data_prep_web
import numpy as np
from typing import Tuple

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load race, web, and wiki data from parquet files.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: DataFrames containing race, web, and wiki data.
    """
    df_race = pd.read_parquet(c.race_2024_path)
    df_web = pd.read_parquet(c.web_2024_path)
    df_wiki = pd.read_parquet(c.wiki_2024_path)
    return df_race, df_web, df_wiki


def merge_datasets(df_race: pd.DataFrame, df_web: pd.DataFrame, df_wiki: pd.DataFrame) -> pd.DataFrame:
    """
    Merge race, web, and wiki datasets on the skipper column.

    Args:
        df_race (pd.DataFrame): Race data.
        df_web (pd.DataFrame): Processed web data.
        df_wiki (pd.DataFrame): Wiki data.

    Returns:
        pd.DataFrame: Merged dataset.
    """
    df = pd.merge(df_race, df_web, on="skipper", how="left")
    df = pd.merge(df, df_wiki, on="skipper", how="left")
    return df

def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the dataset into dynamic race data and static info data.

    Args:
        df (pd.DataFrame): The merged dataset.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Separated race and info datasets.
    """
    dynamic_cols = [
        "rang", "heure", "latitude", "longitude", "cap_30min", "vitesse_30min", "VMG_30min", "distance_30min",
        "cap_last", "vitesse_last", "VMG_last", "distance_last", "cap_24h", "vitesse_24h", "VMG_24h", "distance_24h",
        "DTF", "DTL", "date"
    ]
    static_cols = [col for col in df.columns if col not in dynamic_cols]
    return df[dynamic_cols].copy(), df[static_cols].copy()

def clean_and_rename(df_race: pd.DataFrame, df_infos: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Rename columns and clean the datasets.

    Args:
        df_race (pd.DataFrame): Race dataset.
        df_infos (pd.DataFrame): Info dataset.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Cleaned and renamed race and info datasets.
    """
    rename_dict = {
        "rang": "rank", "heure": "time", "latitude": "latitude", "longitude": "longitude",
        "cap_30min": "heading_30min", "vitesse_30min": "speed_30min", "VMG_30min": "vmg_30min", "distance_30min": "distance_30min",
        "cap_last": "heading_last", "vitesse_last": "speed_last", "VMG_last": "vmg_last", "distance_last": "distance_last",
        "cap_24h": "heading_24h", "vitesse_24h": "speed_24h", "VMG_24h": "vmg_24h", "distance_24h": "distance_24h",
        "DTF": "distance_to_finish", "DTL": "distance_to_leader", "date": "date"
    }
    df_race.rename(columns=rename_dict, inplace=True)
    df_infos.rename(columns=rename_dict, inplace=True)
    return df_race, df_infos

def merge_duplicate_columns(df_infos: pd.DataFrame) -> pd.DataFrame:
    """
    Merge duplicate columns (_x and _y versions) and remove unnecessary suffixes.

    Args:
        df_infos (pd.DataFrame): Info dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    cols_x = [col for col in df_infos.columns if col.endswith('_x')]
    for col in cols_x:
        col_y = col.replace('_x', '_y')
        if col_y in df_infos.columns:
            df_infos[col] = df_infos[col].combine_first(df_infos[col_y])
            df_infos.drop(columns=[col_y], inplace=True)
        df_infos.rename(columns={col: col.replace('_x', '')}, inplace=True)
    df_infos.columns = [col.replace("_y", "") for col in df_infos.columns]
    df_infos.drop_duplicates(inplace=True)
    return df_infos

def add_batch_column(df_race: pd.DataFrame) -> pd.DataFrame:
    """
    Add a batch column based on the date column.

    Args:
        df_race (pd.DataFrame): Race dataset.

    Returns:
        pd.DataFrame: Dataset with batch column added.
    """
    df_race = df_race.sort_values(by="date")
    df_race["batch"] = df_race["date"].ne(df_race["date"].shift()).cumsum() - 1
    return df_race

if __name__ == "__main__":
    df_race, df_web, df_wiki = load_data()
    df_web = data_prep_web(df_web, skipper_corrections=[('Kojiro Shiraishi', 'Kōjirō Shiraishi')])
    df = merge_datasets(df_race, df_web, df_wiki)
    df_race, df_infos = split_data(df)
    df_race, df_infos = clean_and_rename(df_race, df_infos)
    df_infos = merge_duplicate_columns(df_infos)
    df_infos= df_infos.map(lambda x: None if pd.isna(x) else x)
    df_infos.replace([np.inf, -np.inf], np.nan).isna().sum()
    df_race = add_batch_column(df_race)

    df_race.to_parquet(c.df_race_path, engine="pyarrow", index=False)
    df_infos.to_parquet(c.df_infos_path, engine="pyarrow", index=False)