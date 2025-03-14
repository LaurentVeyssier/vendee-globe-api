# Vendée Globe API

**Vendée Globe API** is a FastAPI-based RESTful API that provides race data and information about skippers and boats.  
This project is designed to track race progress, update batch data dynamically, and serve static boat/skipper details.

## 🚀 Features
- **Race Tracking**: Get dynamic race data with batch updates every 2 minutes.
- **Skipper & Boat Information**: Retrieve static information about participants and their boats.
- **Optimized Performance**: Pre-cleaned datasets for efficient querying.
- **Automated Batch Update**: Background task increments batch index every 2 minutes.

---

## 📦 Installation

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/vendee-globe-api.git
cd vendee-globe-api
```

### **2. Create and activate a virtual environment with UV**

run : 
`curl -LsSf https://astral.sh/uv/install.sh | sh`

then run :   `uv sync`

finaly : `source .venv/bin/activate`

### **3. Start the API**

`uvicorn main:app --reload`

## Example Request 

GET /infos : Returns static information about skippers and boats.
```bash
curl -X GET http://127.0.0.1:8000/infos
```

GET /race : Returns all race data batches up to the current batch index.
```bash
curl -X GET http://127.0.0.1:8000/race
```

The race data batches update automatically every 2 minutes.

	•	The batch index starts at 0.
	•	Every 120 seconds, a background task increments the current batch index.
	•	New data becomes available in /race endpoint as batches progress.


