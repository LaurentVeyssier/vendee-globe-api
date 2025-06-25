# Vendée Globe API

**Vendée Globe API** is a FastAPI-based RESTful API that provides race data and information about skippers and boats.
This project is designed to track race progress, update batch data dynamically, and serve static boat/skipper details.

## Features

- **Race Tracking**: Get dynamic race data with batch updates every few seconds.
- **Skipper & Boat Information**: Retrieve static information about participants and their boats.
- **Optimized Performance**: Pre-cleaned datasets for efficient querying.
- **Automated Batch Update**: Background task increments batch index every few seconds.

---

## Installation

### **1. Clone the repository**

```bash
git clone https://github.com/datacraft-paris/vendee-globe-api.git
cd vendee-globe-api
```

### **2. Create and activate a virtual environment with UV**

### **Navigate to the Project Directory**

Before executing the following commands, ensure you are in the project directory and have checked out the correct branch:

```bash
git checkout <branch-name>
```

Replace `<branch-name>` with the branch you want to work on.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
source .venv/bin/activate
```

### **3. Set your timer parameter**

In `config.yaml`, set your timer value.
The time value defines the time required, in minutes, for the API to display all data.
For a good refresh rate, something between 30 and 60 minutes is pretty good.

### **4. Start the API**

```bash
fastapi dev src/vendee_globe_api/main.py
```

## Example Request

### **Write and Test Requests in Another Terminal**

To test the API endpoints, open a new terminal window while keeping the server running. Use the following examples to make requests:

#### Example 1: Fetch Static Information

GET /infos : Retrieve details about skippers and boats:

```bash
curl -X GET http://127.0.0.1:8000/boats
```

#### Example 2: Fetch Race Data

GET /race : Retrieve all race data batches up to the current batch index:

```bash
curl -X GET http://127.0.0.1:8000/race
```
