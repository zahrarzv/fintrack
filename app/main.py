from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

from app.categorize import categorize
from app.db import insert_transaction, list_transactions, monthly_summary

app = FastAPI(title="FinTrack API")


class TxCreate(BaseModel):
    tx_date: str = Field(..., description="YYYY-MM-DD")
    merchant: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    tx_type: Literal["expense", "income"]


class TxCreateResponse(BaseModel):
    id: int
    category: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=TxCreateResponse)
def create_transaction(tx: TxCreate):
    amount_cents = int(round(tx.amount * 100))
    if amount_cents <= 0:
        raise HTTPException(status_code=400, detail="Amount must be > 0")

    cat = categorize(tx.merchant, tx.tx_type)
    new_id = insert_transaction(tx.tx_date, tx.merchant, amount_cents, tx.tx_type, cat)
    return {"id": new_id, "category": cat}


@app.get("/transactions")
def get_transactions(month: Optional[str] = None, category: Optional[str] = None):
    return {"transactions": list_transactions(month=month, category=category)}


@app.get("/summary")
def get_summary(month: str):
    # month: YYYY-MM
    return monthly_summary(month)
