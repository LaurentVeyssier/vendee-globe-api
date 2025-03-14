import logging
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import pandas as pd
import constants as c
import numpy as np
import asyncio
from datetime import timedelta

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

try:
    # Charger les datasets
    logger.info("Chargement des datasets...")
    df_infos = pd.read_parquet(c.df_infos_path)
    df_race = pd.read_parquet(c.df_race_path)
    logger.info("Datasets chargés avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement des datasets : {e}", exc_info=True)

# Index du batch actuel
current_batch_index = 0
batch_interval = timedelta(minutes=2)

@app.get("/infos")
def get_infos():
    """
    Endpoint pour récupérer les informations statiques sur les skippers et les bateaux.
    """
    try:
        logger.info("Requête reçue sur /infos")
        
        # Vérifier les valeurs NaN
        nan_counts = df_infos.isna().sum()
        if nan_counts.sum() > 0:
            logger.warning(f"🚨 Présence de NaN dans df_infos :\n{nan_counts[nan_counts > 0]}")
        
        # Vérifier les valeurs infinies
        inf_counts = (df_infos == np.inf).sum() + (df_infos == -np.inf).sum()
        if inf_counts.sum() > 0:
            logger.warning(f"🚨 Présence de valeurs infinies dans df_infos :\n{inf_counts[inf_counts > 0]}")
        
        # Correction des valeurs problématiques
        df_cleaned = df_infos.copy()
        df_cleaned.replace([np.inf, -np.inf], None, inplace=True)  # Remplacer `inf` par `None`

        # Convertir les colonnes numériques en str avant de remplacer les NaN
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype == "float64":  # Éviter le FutureWarning de Pandas
                df_cleaned[col] = df_cleaned[col].astype(str).replace("nan", "N/A")
            else:
                df_cleaned[col] = df_cleaned[col].fillna("N/A")

        return df_cleaned.to_dict(orient="records")
    
    except Exception as e:
        logger.error(f"Erreur dans l'endpoint /infos : {e}", exc_info=True)
        return {"error": "Erreur interne, voir logs pour plus de détails."}

@app.get("/race")
def get_race():
    """
    Endpoint pour récupérer tous les batches de données dynamiques jusqu'au batch actuel.
    """
    global current_batch_index
    try:
        logger.info(f"Requête reçue sur /race avec current_batch_index={current_batch_index}")
        
        unique_batches = df_race["batch"].unique()
        logger.info(f"Nombre total de batches disponibles : {len(unique_batches)}")
        
        if current_batch_index >= len(unique_batches):
            logger.warning("Tentative d'accès aux données après la fin des batches disponibles.")
            return {"message": "Fin des données disponibles"}
        
        batch_values = unique_batches[:current_batch_index + 1]
        batch_data = df_race[df_race["batch"].isin(batch_values)]
        
        logger.info(f"Retour des données jusqu'au batch {current_batch_index}")
        return batch_data.to_dict(orient="records")
    
    except Exception as e:
        logger.error(f"Erreur dans l'endpoint /race : {e}", exc_info=True)
        return {"error": "Erreur interne, voir logs pour plus de détails."}

async def batch_scheduler():
    """
    Programmeur de tâches manuel pour mettre à jour les batches toutes les 2 minutes.
    """
    global current_batch_index
    while True:
        await asyncio.sleep(120)  # Attendre 2 minutes
        try:
            unique_batches = df_race["batch"].unique()
            max_batches = len(unique_batches)
            
            if current_batch_index < max_batches - 1:
                current_batch_index += 1
                logger.info(f"✅ Batch index mis à jour : {current_batch_index}")
            else:
                logger.warning("⚠️ Tentative de mise à jour au-delà des données disponibles.")
        
        except Exception as e:
            logger.error(f"❌ Erreur dans batch_scheduler : {e}", exc_info=True)

# Lancer le scheduler au démarrage
@app.on_event("startup")
async def startup_event():
    logger.info("🔄 Démarrage de la tâche batch_scheduler...")
    asyncio.create_task(batch_scheduler())