import logging
from fastapi import FastAPI
import pandas as pd
import constants as c
import numpy as np
import asyncio

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

try:
    # Load datasets
    logger.info("Loading datasets...")
    df_infos = pd.read_parquet(c.df_infos_path)
    df_race = pd.read_parquet(c.df_race_path)
    logger.info("Datasets successfully loaded.")
except Exception as e:
    logger.error(f"Error loading datasets: {e}", exc_info=True)

# Batch index tracking
current_batch_index = 0

@app.get("/infos")
def get_infos():
    """
    Returns static information about skippers and boats.
    """
    try:
        logger.info("Request received on /infos")
        return df_infos.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error in /infos endpoint: {e}", exc_info=True)
        return {"error": "Internal server error. Check logs for details."}

@app.get("/race")
def get_race():
    """
    Returns all race data batches up to the current batch index.
    """
    global current_batch_index
    try:
        logger.info(f"Request received on /race (current_batch_index={current_batch_index})")

        unique_batches = df_race["batch"].unique()
        total_batches = len(unique_batches)
        logger.info(f"Total available batches: {total_batches}")

        if current_batch_index >= total_batches:
            logger.warning("Attempted to access data beyond available batches.")
            return {"message": "No more available data."}

        batch_values = unique_batches[:current_batch_index + 1]
        batch_data = df_race[df_race["batch"].isin(batch_values)]

        logger.info(f"Returning data up to batch {current_batch_index}")
        return batch_data.to_dict(orient="records")

    except Exception as e:
        logger.error(f"Error in /race endpoint: {e}", exc_info=True)
        return {"error": "Internal server error. Check logs for details."}

async def batch_scheduler():
    """
    Updates the batch index every 2 minutes.
    """
    global current_batch_index
    unique_batches = df_race["batch"].unique()
    total_batches = len(unique_batches)

    while True:
        await asyncio.sleep(120)
        try:
            if current_batch_index < total_batches - 1:
                current_batch_index += 1
                logger.info(f"Batch index updated: {current_batch_index}")
            else:
                logger.warning("Batch index update attempted beyond available data.")
        except Exception as e:
            logger.error(f"Error in batch_scheduler: {e}", exc_info=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting batch scheduler...")
    asyncio.create_task(batch_scheduler())