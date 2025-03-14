from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import pandas as pd
import constants as c
from datetime import timedelta

app = FastAPI()

# Charger les datasets
df_infos = pd.read_parquet(c.df_infos_path)
df_race = pd.read_parquet(c.df_race_path)

# Index du batch actuel
current_batch_index = 0
batch_interval = timedelta(minutes=2)

@app.get("/infos")
def get_infos():
    """
    Endpoint pour récupérer les informations statiques sur les skippers et les bateaux.
    """
    return df_infos.to_dict(orient="records")

@app.get("/race")
def get_race():
    """
    Endpoint pour récupérer tous les batches de données dynamiques jusqu'au batch actuel.
    """
    global current_batch_index
    
    # Sélectionner les batchs jusqu'à l'index actuel
    unique_batches = df_race["batch"].unique()
    if current_batch_index >= len(unique_batches):
        return {"message": "Fin des données disponibles"}
    
    batch_values = unique_batches[:current_batch_index + 1]
    batch_data = df_race[df_race["batch"].isin(batch_values)]
    
    return batch_data.to_dict(orient="records")

@repeat_every(seconds=120) 
async def batch_updater():
    """
    Tâche asynchrone pour mettre à jour les batches toutes les 2 minutes.
    """
    global current_batch_index
    current_batch_index += 1
