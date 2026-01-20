from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
import psycopg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Put it in your .env file.")


@dataclass
class TxRow:
    id: int
    tx_date: str
    merchant: str
    amount_cents: int
    tx_type: str
    category: str


def get_conn():
    return psycopg.connect(DATABASE_URL)


def insert_transaction(tx_date: str, merchant: str, amount_cents: int, tx_type: str, category: str) -> int:
    q = """
    INSERT INTO transactions (tx_date, merchant, amount_cents, tx_type, category)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(q, (tx_date, merchant, amount_cents, tx_type, category))
            new_id = cur.fetchone()[0]
            return int(new_id)


def list_transactions(month: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    # month format: YYYY-MM
    where = []
    params: List[Any] = []

    if month:
        where.append("to_char(tx_date, 'YYYY-MM') = %s")
        params.append(month)
    if category:
        where.append("category = %s")
        params.append(category)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    q = f"""
    SELECT id, tx_date, merchant, amount_cents, tx_type, category
    FROM transactions
    {where_sql}
    ORDER BY tx_date DESC, id DESC;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(q, params)
            rows = cur.fetchall()

    out = []
    for r in rows:
        out.append({
            "id": r[0],
            "tx_date": str(r[1]),
            "merchant": r[2],
            "amount": r[3] / 100.0,
            "tx_type": r[4],
            "category": r[5],
        })
    return out


def monthly_summary(month: str) -> Dict[str, Any]:
    # totals
    q_totals = """
    SELECT
      COALESCE(SUM(CASE WHEN tx_type='expense' THEN amount_cents ELSE 0 END), 0) AS expense_cents,
      COALESCE(SUM(CASE WHEN tx_type='income' THEN amount_cents ELSE 0 END), 0) AS income_cents
    FROM transactions
    WHERE to_char(tx_date, 'YYYY-MM') = %s;
    """

    # category breakdown (expenses only)
    q_cats = """
    SELECT category, SUM(amount_cents) AS cents
    FROM transactions
    WHERE to_char(tx_date, 'YYYY-MM') = %s
      AND tx_type = 'expense'
    GROUP BY category
    ORDER BY cents DESC;
    """

    # top merchants (expenses only)
    q_merchants = """
    SELECT merchant, SUM(amount_cents) AS cents
    FROM transactions
    WHERE to_char(tx_date, 'YYYY-MM') = %s
      AND tx_type = 'expense'
    GROUP BY merchant
    ORDER BY cents DESC
    LIMIT 5;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(q_totals, (month,))
            expense_cents, income_cents = cur.fetchone()

            cur.execute(q_cats, (month,))
            cats = [{"category": c, "amount": cents / 100.0} for (c, cents) in cur.fetchall()]

            cur.execute(q_merchants, (month,))
            merchants = [{"merchant": m, "amount": cents / 100.0} for (m, cents) in cur.fetchall()]

    return {
        "month": month,
        "total_expense": expense_cents / 100.0,
        "total_income": income_cents / 100.0,
        "net": (income_cents - expense_cents) / 100.0,
        "by_category": cats,
        "top_merchants": merchants,
    }
