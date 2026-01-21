
# FinTrack — Local Setup & Run Instructions

This guide explains how to run FinTrack locally (PostgreSQL + FastAPI API + Streamlit dashboard).

---

##  Prerequisites

- Python 3.11+ (works on Python 3.13)
- Docker Desktop (for PostgreSQL)
- Git (optional)

---

## 1 Start PostgreSQL (Docker)

From the project root:

```bash
docker compose up -d

# Apply the schema
docker compose exec -T db psql -U postgres -d fintrack < app/schema.sql

#Verify the table exists:
docker compose exec -T db psql -U postgres -d fintrack -c "\dt"

# create .env file
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fintrack

# install Dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the fastAPI backend

python -m uvicorn app.main:app --reload

#Swagger docs: http://127.0.0.1:8000/docs
#health check: http://127.0.0.1:8000/health

# Run the Streamlit Dashboard 
source .venv/bin/activate
streamlit run dashboard.py

# open: http://localhost:8501

# Run tests
pytest -q

# make sure the API is running: 
python -m uvicorn app.main:app --reload
# Make sure Postgres is running:
docker compose ps




#Restart if needed:
docker compose down
docker compose up -d


## Performance Benchmark 

##This project includes a small benchmark script to measure the response time of the monthly summary endpoint.

### 1) Start the API
```bash
python -m uvicorn app.main:app --reload

# in a new terminal, Run the benchmark
python scripts/benchmark_summary.py

# The script measures GET /summary?month=2026-01 for 30 runs and prints p50/p95 latency.

