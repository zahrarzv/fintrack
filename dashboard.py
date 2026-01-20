import httpx
import streamlit as st
import pandas as pd
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def api_get(path, params=None):
    try:
        r = httpx.get(f"{API_URL}{path}", params=params, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not reach API at {API_URL}. Is uvicorn running?\n\nError: {e}")
        return None

# ... keep your UI code above ...

month = st.text_input("Month (YYYY-MM)", value=pd.Timestamp.today().strftime("%Y-%m"))

summary = api_get("/summary", params={"month": month})
if summary:
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${summary['total_income']:.2f}")
    col2.metric("Expenses", f"${summary['total_expense']:.2f}")
    col3.metric("Net", f"${summary['net']:.2f}")

    st.subheader("Spending by Category")
    df_cats = pd.DataFrame(summary["by_category"])
    if not df_cats.empty:
        st.bar_chart(df_cats.set_index("category")["amount"])
    else:
        st.info("No expense data for this month yet.")

    st.subheader("Top Merchants")
    st.dataframe(pd.DataFrame(summary["top_merchants"]), use_container_width=True)

txs = api_get("/transactions", params={"month": month})
if txs:
    st.subheader("Recent Transactions")
    st.dataframe(pd.DataFrame(txs["transactions"]), use_container_width=True)
