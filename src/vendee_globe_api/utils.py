import pandas as pd
import numpy as np
import plotly.express as px
from typing import List, Optional


def clean_skipper_names(df: pd.DataFrame, skipper_corrections: List[tuple]) -> pd.DataFrame:
    """Standardize skipper names and apply corrections."""
    if "skipper" not in df:
        df["skipper"] = df["first_name"].str.strip() + " " + df["last_name"].str.strip()
    for old_name, new_name in skipper_corrections:
        df['skipper'] = df['skipper'].replace(old_name, new_name)
    return df


def convert_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Convert specified columns to numeric format, handling missing values and formatting issues."""
    for col in columns:
        if col in df:
            df[col] = df[col].fillna('').str.extract(r'([\d,]+)')[0]
            df[col] = df[col].str.replace(',', '.').replace('', np.nan).replace('NC', np.nan).astype(float)
    return df


def clean_architect_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize architect names by formatting separators consistently."""
    if "Architecte" in df:
        df["Architecte"] = (df["Architecte"].str.strip()
                             .str.replace(r"[/–]", "-", regex=True)
                             .str.replace(r" ?- ?", " - ", regex=True))
    return df


def data_prep_web(df: pd.DataFrame, skipper_corrections: Optional[List[tuple]] = None) -> pd.DataFrame:
    """Prepare web data by standardizing skipper names, converting numeric columns, and cleaning architect names."""
    skipper_corrections = skipper_corrections or []
    df = clean_skipper_names(df, skipper_corrections)
    df = convert_numeric_columns(df, ['Longueur', 'Largeur', "Tirant d'eau", "Déplacement (poids)",
                                      "Hauteur mât", "Surface de voiles au près", "Surface de voiles au portant", "Poids"])
    df = clean_architect_names(df)
    return df


def parse_lat_lon(coord: pd.Series, direction_map: dict) -> pd.Series:
    """Convert latitude or longitude from degrees and minutes format to decimal format."""
    tab = coord.str.extract(r"(\d+)°([\d\.]+)'([NSWE])")
    return (tab[0].astype(float) + tab[1].astype(float) / 60) * tab[2].map(direction_map)


def data_prep_race(df: pd.DataFrame, skipper_corrections: Optional[List[tuple]] = None) -> pd.DataFrame:
    """Prepare race data by formatting numeric columns, parsing dates, cleaning skipper names, and converting coordinates."""
    skipper_corrections = skipper_corrections or []
    
    numeric_cols = ['cap_30min', 'vitesse_30min', 'VMG_30min', 'distance_30min',
                    'cap_last', 'vitesse_last', 'VMG_last', 'distance_last',
                    'cap_24h', 'vitesse_24h', 'VMG_24h', 'distance_24h',
                    'DTF', 'DTL']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d_%H%M%S', errors='coerce')
    
    df[['nat', 'voile']] = df['nat_voile'].str.extract(r'([A-Z]{3})\s*(\d+)')
    df['nat_voile'] = df['nat'] + df['voile']
    
    df[['skipper', 'voilier']] = df['skipper_voilier'].str.title().str.split('\n', expand=True)
    df = clean_skipper_names(df, skipper_corrections)
    
    df['latitude'] = parse_lat_lon(df['latitude'], {'N': 1, 'S': -1})
    df['longitude'] = parse_lat_lon(df['longitude'], {'E': 1, 'W': -1})
    
    skippers = df['skipper'].dropna().unique()
    colors = (px.colors.qualitative.Plotly * 4)[:len(skippers)]
    df['color'] = df['skipper'].map(dict(zip(skippers, colors)))
    
    return df