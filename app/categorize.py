from __future__ import annotations

RULES = {
    "uber": "Transit",
    "lyft": "Transit",
    "shell": "Gas",
    "esso": "Gas",
    "walmart": "Groceries",
    "no frills": "Groceries",
    "superstore": "Groceries",
    "starbucks": "Coffee",
    "tim hortons": "Coffee",
    "amazon": "Shopping",
    "netflix": "Subscriptions",
    "spotify": "Subscriptions",
    "rent": "Rent",
}

DEFAULT_EXPENSE_CATEGORY = "Other"
DEFAULT_INCOME_CATEGORY = "Income"


def categorize(merchant: str, tx_type: str) -> str:
    m = merchant.strip().lower()
    if tx_type == "income":
        return DEFAULT_INCOME_CATEGORY
    for key, cat in RULES.items():
        if key in m:
            return cat
    return DEFAULT_EXPENSE_CATEGORY
