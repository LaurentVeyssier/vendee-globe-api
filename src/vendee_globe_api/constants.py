from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent

db_path = root_dir / "data" / "vendee_globe.sqlite"

race_2024_path = root_dir / "data" / "race_2024.parquet"
web_2024_path = root_dir / "data" / "web_2024.parquet"
wiki_2024_path = root_dir / "data" / "wiki_2024.parquet"

df_race_path = root_dir / "data" / "df_race.parquet"
df_infos_path = root_dir / "data" / "df_infos.parquet"

# TODO: define database url, database is in data/vendee_globe.sqlite
DATABASE_URL = ...
