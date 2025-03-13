from fastapi import FastAPI
import pandas as pd
import asyncio
import constants as c

df = pd.read_parquet(c.race_2024_path)

app = FastAPI()

current_time = df["heure"].min()
time_step = pd.Timedelta(minutes=2) 

@app.get("/race")
def get_next_batch():
    global current_time
    
    # Filtrer les données du batch actuel
    batch = df[df["heure"] == current_time]
    
    # Avancer au prochain batch simulé
    next_time = current_time + time_step
    if next_time in df["heure"].values:
        current_time = next_time
    
    return batch.to_dict(orient="records")