import logging
from fastapi import FastAPI
import pandas as pd
import constants as c
import numpy as np
import asyncio

"""
FastAPI application for the Vendée Globe API.
For more information or explanations about the code, you can refer to the `explanations_code.md` document.
"""

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI() # API instance

@app.get("/") # Root endpoint 
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Bienvenue sur l'API Vendée Globe"}

"""
Load datasets with try-except for error handling.
- df_infos: Contains information about skippers and boats.
- df_race: Contains information about race data.
"""
try:
    # Load datasets
    logger.info("Loading datasets...")
    df_infos = pd.read_parquet(c.df_infos_path) # Importing the skippers and boats data into a DataFrame
    df_race = pd.read_parquet(c.df_race_path) # Importing the race data into a DataFrame
    logger.info("Datasets successfully loaded.")
except Exception as e:
    logger.error(f"Error loading datasets: {e}", exc_info=True) # Handle loading errors

# Batch index tracking
current_batch_index = 0

@app.get("/infos") # Endpoint to get skipper and boat information
def get_infos():
    """
    Returns all skipper and boat information with the latest data.
     
    """
    try:
        logger.info("Request received on /infos")
        return df_infos.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error in /infos endpoint: {e}", exc_info=True) # Handle errors
        return {"error": "Internal server error. Check logs for details."} # Send error message to the client

@app.get("/race") # Endpoint to get race data wrt the current batch index
def get_race():
    """
    Returns all race data batches up to the current batch index.
    """
    global current_batch_index
    try:
        logger.info(f"Request received on /race (current_batch_index={current_batch_index})")

        unique_batches = df_race["batch"].unique() # Get unique batch values
        total_batches = len(unique_batches) # Get the total number of batches
        logger.info(f"Total available batches: {total_batches}")

        if current_batch_index >= total_batches: # Check if the current batch index exceeds the total number of batches
            logger.warning("Attempted to access data beyond available batches.")
            return {"message": "No more available data."}

        batch_values = unique_batches[:current_batch_index + 1] # Get batch values up to the current index
        batch_data = df_race[df_race["batch"].isin(batch_values)] # Filter the DataFrame to include only the selected batches

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
    unique_batches = df_race["batch"].unique() # Get unique batch values
    total_batches = len(unique_batches) # Get the total number of batches

    while True:
        await asyncio.sleep(5) # Sleep for 5 seconds 
        try:
            if current_batch_index < total_batches - 1: # Check if the current batch index is less than the total number of batches
                current_batch_index += 1 # Increment the batch index
                logger.info(f"Batch index updated: {current_batch_index}")
            else:
                logger.warning("Batch index update attempted beyond available data.")
        except Exception as e:
            logger.error(f"Error in batch_scheduler: {e}", exc_info=True)

@app.on_event("startup") # Event triggered when the application starts
async def startup_event(): # async function to run on startup
    logger.info("Starting batch scheduler...")
    asyncio.create_task(batch_scheduler()) # Start the batch scheduler in the background