import sqlite3

import pandas as pd

if __name__ == "__main__":
    # Load the Parquet file into a DataFrame
    df_boats = pd.read_parquet(
        "./data/df_infos.parquet"
    )  # Uses pyarrow or fastparquet backend
    df_race = pd.read_parquet(
        "./data/df_race.parquet"
    )  # Uses pyarrow or fastparquet backend
    # Connect to a new SQLite database (or open if exists)
    conn = sqlite3.connect("./data/vendee_globe.sqlite")

    # Write the DataFrame to a new table
    df_boats.to_sql("boats", conn, if_exists="replace", index=False)
    df_race.to_sql("race", conn, if_exists="replace", index=True, index_label="id")

    # (Optional) Close connection
    conn.close()
