# FinTrack  — Expense Tracker & Insights Dashboard

FinTrack is a simple fintech-style project that lets users log transactions, automatically categorize spending, and view monthly insights (income, expenses, net, category breakdown, top merchants) through a Streamlit dashboard.

This project was built to demonstrate practical backend engineering skills: API design, data modeling, input validation, testing, and a user-facing analytics dashboard.

---

##  What It Does

- **Log transactions** (income/expense) with validation
- **Auto-categorize merchants** using rule-based matching (e.g., Uber → Transit, Starbucks → Coffee)
- **View insights by month**
  - total income, total expenses, net
  - spending by category
  - top merchants
- **Browse transaction history** with filters (month, category)

---

##  Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **DB Driver:** psycopg
- **Dashboard:** Streamlit
- **Testing:** pytest
- **Local Dev:** Docker Compose

---

## Dashboard Preview

![FinTrack Dashboard](images/dashboard.png)

---

##  API Endpoints (High-Level)

- `POST /transactions` — create a transaction (category auto-assigned)
- `GET /transactions` — list transactions (optional filters: month, category)
- `GET /summary?month=YYYY-MM` — monthly totals + category breakdown + top merchants

---

## What I’d Improve Next

- CSV import (upload bank export file and auto-ingest transactions)
- Smarter categorization (learn from user overrides)
- Authentication (simple user accounts)
- Deployment (Render/Fly.io + managed Postgres)

---

## Notes

This project is for educational/demo purposes and does not handle real banking credentials or sensitive financial integrations.
