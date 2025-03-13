import pandas as pd
import constants as c

df_race = pd.read_parquet(c.race_2024_path)
df_web = pd.read_parquet(c.web_2024_path)
df_web = vg.data_prep_web(df_web, skipper_corrections=[('Kojiro Shiraishi', 'Kōjirō Shiraishi')])
