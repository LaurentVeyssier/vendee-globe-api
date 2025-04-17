
# 🧠 `explanations_code.md`

This document explains the structure and logic of the FastAPI Vendée Globe API project.

---

## 🚀 Imports and Initial Configuration
```python
import logging
from fastapi import FastAPI
import pandas as pd
import constants as c
import numpy as np
import asyncio
```
- **`import logging`**: Python module for logging messages.
- **`from fastapi import FastAPI`**: FastAPI is used to create the web API.
- **`import pandas as pd`**: For handling tabular data.
- **`import constants as c`**: Loads local constants like file paths.
- **`import numpy as np`**: NumPy is used for numerical operations.
- **`import asyncio`**: Enables asynchronous programming (non-blocking tasks).

---

## 🧾 Logger Configuration
```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
```
- The first line sets up global logging behavior (level and format).
- The second line creates a logger specific to the current module, which you can use to log messages.

### Code Explanation

- **`logging.basicConfig(...)`**: This function configures the root logger, which is the default logger used by the logging module. It sets global logging settings, such as the logging level and the format of log messages.
- **`level=logging.INFO`**: Sets the logging level to INFO.
Only log messages with a severity of INFO or higher (WARNING, ERROR, CRITICAL) will be processed and displayed. Lower-severity messages like DEBUG will be ignored.
- **`format="%(asctime)s - %(levelname)s - %(message)s"`**: Specifies the format of log messages.
  - `%(asctime)s`: Timestamp of when the log message was created.
  - `%(levelname)s`: Severity level of the log message (e.g., INFO, ERROR).
  - `%(message)s`: The actual log message content.
- **`logger = logging.getLogger(__name__)`**: Creates a logger instance for the current module, use to log messages in your code.
- **`__name__`**: A special variable in Python that holds the name of the current module. If this code is in a file named `app.py`, `__name__` will be `"app"`. If this code is in the main script being executed, __name__ will be "__main__".
Using __name__ ensures that the logger is uniquely named based on the module, which is helpful for debugging in larger applications.
- **`logger.info(...)`**: Logs an informational message.

---

## ⚙️ FastAPI App Instance
```python
app = FastAPI()
```
- Instantiates the FastAPI app.

---

## 📍 Root Endpoint
```python
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Vendée Globe"}
```
- Sets up the logger to print messages with time, severity, and content.
- Uses the module’s name as the logger name.

### Code Explanation

1. **`@app.get("/")`**:
   - This is a **decorator** in Python, provided by FastAPI.
   - It tells FastAPI to associate the following function (`read_root`) with an HTTP `GET` request to the root URL (`"/"`).
   - The root URL (`"/"`) is the base path of the API. For example, if the API is hosted at `http://localhost:8000`, this endpoint will respond to `http://localhost:8000/`.
2. **`def read_root():`**:
   - The Python function `read_root` will be executed whenever a `GET` request is made to the root URL (`"/"`).
3. **`return {"message": "Bienvenue sur l'API Vendée Globe"}`**:
   - The response is a **JSON object** (a dictionary in Python) with a single key-value pair:
     - Key: `"message"`
     - Value: `"Bienvenue sur l'API Vendée Globe"`
   - FastAPI automatically converts the Python dictionary into a JSON response.

### What Happens When Accessed
1. A client (e.g., a browser or a tool like Postman) sends a `GET` request to the root URL (`"/"`).
2. FastAPI routes the request to the `read_root` function.
3. The function executes and returns the JSON response: `{"message": "Bienvenue sur l'API Vendée Globe"}`.
4. FastAPI handles the conversion of the Python data structures (like dictionaries) into JSON format nd sends them back to the client as API responses.

---

## 📂 Dataset Loading
```python
try:
    logger.info("Loading datasets...")
    df_infos = pd.read_parquet(c.df_infos_path)
    df_race = pd.read_parquet(c.df_race_path)
    logger.info("Datasets successfully loaded.")
except Exception as e:
    logger.error(f"Error loading datasets: {e}", exc_info=True)
```
- Loads datasets from Parquet files.
- Logs messages before and after loading.
- Catches and logs any errors with full trace.

### Code Explanation

1. **`try:` Block**:
   - The `try` block is used to wrap the code that might raise an exception. If an exception occurs, the program will jump to the corresponding `except` block.

2. **`logger.info("Loading datasets...")`**:
   - This logs an informational message
   - `logger` is an instance of Python's `logging` module, which is used for tracking events during program execution.

3. **`df_infos = pd.read_parquet(c.df_infos_path)`**:
   - This line uses the `pandas` library (`pd`) to read a Parquet file located at the path specified by `c.df_infos_path`.

4. **`df_race = pd.read_parquet(c.df_race_path)`**:
   - Similarly, this reads another Parquet file from the path `c.df_race_path`.

5. **`except Exception as e:`**:
   - This block catches any exception that occurs in the `try` block. The `Exception` class is the base class for all exceptions in Python, so this will catch any error.

7. **`logger.error(f"Error loading datasets: {e}", exc_info=True)`**:
   - If an exception is caught, this logs an error message with details about the exception (`e`).
   - The `exc_info=True` argument ensures that the full traceback of the exception is included in the log, which is helpful for debugging.

### Key Concepts

- **Error Handling**:
  - The `try-except` structure ensures that the program doesn't crash if an error occurs while loading the datasets. Instead, it logs the error and can continue running or handle the failure gracefully.

- **Logging**:
  - The `logger` object is used to log messages at different severity levels. This is a best practice for monitoring and debugging applications.

- **Parquet Files**:
  - Parquet is a columnar storage file format commonly used for large-scale data processing. The `pandas.read_parquet` function is used to load such files into a DataFrame.

---

## 🔢 Batch Index Initialization
```python
current_batch_index = 0
```
- Global variable to keep track of the current batch index.

---

## 📊 `/infos` Endpoint
```python
@app.get("/infos")
def get_infos():
    try:
        logger.info("Request received on /infos")
        return df_infos.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error in /infos endpoint: {e}", exc_info=True)
        return {"error": "Internal server error. Check logs for details."}
```
- Returns skipper and boat info.
- Converts DataFrame into list of JSON objects.

### Code Explanation

### 1. `@app.get("/infos")`
- This is a **decorator** that registers the function `get_infos()` as a handler for HTTP GET requests to the `/infos` route.

### 2. `return df_infos.to_dict(orient="records")`
- Converts the `df_infos` object (Pandas DataFrame) into a list of dictionaries and returns it as the response.
- `df_infos.to_dict(orient="records")`: Converts each row of the DataFrame `df_infos` into a dictionary, where the keys are column names and the values are the corresponding row values. The result is a list of dictionaries, one for each row.
- FastAPI automatically serializes this Python object (list of dictionaries) into JSON format for the HTTP response.

### 7. `return {"error": "Internal server error. Check logs for details."}`
- Returns a JSON response with an error message if an exception occurs.
- The dictionary `{"error": "Internal server error. Check logs for details."}` is serialized into JSON and sent as the HTTP response. This informs the client that something went wrong on the server.
- logger.error records the complete error details for internal diagnostics, while the return statement delivers a safe, user-friendly message to the client.

---

## 🧭 `/race` Endpoint
```python
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
```
- Handles batch-wise filtering of race data.
- Returns accumulated data up to the current batch index.

### Code Explanation

1. **`@app.get("/race")`**:
   - Registers the `get_race` function as a handler for HTTP GET requests to the `/race` endpoint.

2. **`global current_batch_index`**:
   - Declares that the function will use the global variable `current_batch_index` to track the current batch index.

3. **`unique_batches = df_race["batch"].unique()`**:
   - Retrieves all unique values from the batch column of the df_race DataFrame
   - df_race is assumed to be a pandas DataFrame.The ["batch"] accesses the batch column. The .unique() method returns an array of unique values in that column, ensuring no duplicates.

4. **`total_batches = len(unique_batches)`**:
   - Calculates the total number of unique batches.

5. **`if current_batch_index >= total_batches:`**:
   - Checks if the current batch index exceeds the total number of batches. If so, it logs a warning and returns a message indicating no more data is available.

6. **`batch_values = unique_batches[:current_batch_index + 1]`**:
   - Selects all batch identifiers up to and including the current batch index.

7. **`batch_data = df_race[df_race["batch"].isin(batch_values)]`**:
   - Filters the `df_race` DataFrame to include only rows with batch identifiers in `batch_values`.

8. **`return batch_data.to_dict(orient="records")`**:
   - Converts the filtered DataFrame into a list of dictionaries (one per row) and returns it as the response.
   - df_race["batch"].isin(batch_values) creates a boolean mask where True indicates rows with a batch value in batch_values.
   - df_race[...] applies this mask to filter the DataFrame, returning only the matching rows.

### Key Concepts

- **Batch Filtering**:
  - The endpoint dynamically filters race data based on the current batch index, simulating real-time data updates.

---

## ⏲️ Batch Scheduler
```python
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
```
- Asynchronous function that updates the batch index every 5 seconds.
- Useful for simulating real-time data flow.

### Code Explanation

Sure! Let me break down the key lines of the provided code snippet:

### 1. **`async def batch_scheduler():`**
   - Asynchronous functions (marked with `async`) allow the program to perform non-blocking operations, such as waiting for a timer or I/O operations, without halting the execution of other tasks.

### 2. **`await asyncio.sleep(120)`**
   - Pauses the execution of the function for **5 seconds** without blocking other tasks in the event loop.
   - The `await` keyword is used to asynchronously wait for the sleep operation to complete.

### 3. **`if current_batch_index < total_batches - 1:`**
   - Checks if the current batch index is less than the maximum allowable index (`total_batches - 1`).
   - This ensures the index does not exceed the number of available batches.

### 4. **`current_batch_index += 1`**
   - Increments the global `current_batch_index` by 1, moving to the next batch.

- **Key Concepts**:
  - **Asynchronous Function**: The `async def` keyword defines an asynchronous function, allowing non-blocking execution.
  - **Infinite Loop**: The `while True` loop ensures continuous execution.
  - **Sleep Interval**: `await asyncio.sleep(5)` pauses execution for 5 seconds between updates.
- **Behavior**:
  - Increments `current_batch_index` until it reaches the total number of batches.
  - Logs warnings if updates are attempted beyond available data.
- **Integration**: This function is triggered by the `startup_event` hook to run in the background when the app starts.

---

## 🔄 Startup Event Hook
```python
@app.on_event("startup")
async def startup_event():
    logger.info("Starting batch scheduler...")
    asyncio.create_task(batch_scheduler())
```
- Automatically starts the scheduler when the app launches.

### Code Explanation

#### 1. **`@app.on_event("startup")`**
   - This is a **decorator** provided by FastAPI that registers the function below it (`startup_event`) to be executed when the application starts.
   - The `"startup"` event is triggered once the FastAPI app is fully initialized but before it starts handling requests.

#### 2. **`asyncio.create_task(batch_scheduler())`**
   - `asyncio.create_task()` is used to schedule the execution of an **asynchronous task** (`batch_scheduler()` in this case) in the background.
   - This allows the `batch_scheduler()` to run concurrently with other tasks in the application without blocking the main thread.

---
