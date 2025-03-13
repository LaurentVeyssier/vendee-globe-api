import pandas as pd
import constants as c
from utils import data_prep_web

#region load data
df_race = pd.read_parquet(c.race_2024_path)
df_web = pd.read_parquet(c.web_2024_path)
df_wiki = pd.read_parquet(c.wiki_2024_path)

#region data prep
df_web = data_prep_web(df_web, skipper_corrections=[('Kojiro Shiraishi', 'Kōjirō Shiraishi')])

df = pd.merge(df_race, df_web, on="skipper", how="left")
df = pd.merge(df, df_wiki, on="skipper", how="left")

print(df.head())