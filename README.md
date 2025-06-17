# Vendée Globe API

**Vendée Globe API** is a FastAPI-based RESTful API that provides race data and information about skippers and boats.  
This project is designed to track race progress, update batch data dynamically, and serve static boat/skipper details.

## Features
- **Race Tracking**: Get dynamic race data with batch updates every 5 seconds.
- **Skipper & Boat Information**: Retrieve static information about participants and their boats.
- **Optimized Performance**: Pre-cleaned datasets for efficient querying.
- **Automated Batch Update**: Background task increments batch index every 5 seconds.

---

## Installation

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/vendee-globe-api.git
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

### **3. Start the API**
```bash
cd src/vendee_globe_api/
uvicorn main:app --reload
```

## Example Request 
### **Write and Test Requests in Another Terminal**

To test the API endpoints, open a new terminal window while keeping the server running. Use the following examples to make requests:

#### Example 1: Fetch Static Information
GET /infos : Retrieve details about skippers and boats:
```bash
curl -X GET http://127.0.0.1:8000/infos
```

#### Example 2: Fetch Race Data
GET /race : Retrieve all race data batches up to the current batch index:
```bash
curl -X GET http://127.0.0.1:8000/race
```

The race data batches update automatically every 5 seconds.

<ul class="nocopy" style="list-style: disc; padding-left: 20px;">
  <li>Le compteur de batch commence à 0.</li>
  <li>Toutes les 5 secondes, une tâche en arrière-plan incrémente l’index courant.</li>
  <li>De nouvelles données deviennent accessibles sur l’endpoint <code>/race</code> à mesure que les batchs avancent.</li>
</ul>

## Code Explanation

For detailed information and explanations about the codebase, please refer to the [`explanations_code.md`](explanations_code.md) file. This document provides insights into the project structure, main modules, and key implementation details to help you understand and contribute to the Vendée Globe API.
