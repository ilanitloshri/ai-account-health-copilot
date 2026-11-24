# app.py
# The AI Account Health Copilot web app.
# Step 1: show the book of business, with filters and headline numbers.
# Run it with:  .venv/bin/streamlit run app.py

from datetime import date

import pandas as pd
import streamlit as st

# The date the made-up data is "as of" (matches generate_data.py)
DATA_AS_OF = date(2026, 11, 24)

st.set_page_config(page_title="AI Account Health Copilot", layout="wide")


@st.cache_data  # read the file once, not on every click
def load_accounts():
    """Read the account file and add a few helpful calculated columns."""
    accounts = pd.read_csv(
        "data/accounts.csv",
        parse_dates=["contract_start", "renewal_date", "last_qbr_date", "last_sponsor_call_date"],
    )
    as_of = pd.Timestamp(DATA_AS_OF)
    accounts["days_to_renewal"] = (accounts["renewal_date"] - as_of).dt.days
    accounts["days_since_sponsor_call"] = (as_of - accounts["last_sponsor_call_date"]).dt.days
    accounts["seat_use_pct"] = (accounts["seats_active"] / accounts["seats_purchased"] * 100).round()
    return accounts


accounts = load_accounts()

# ---- Header ----
st.title("AI Account Health Copilot")
st.caption(f"Book of business for a Strategic CSM · fictional data as of {DATA_AS_OF:%B %d, %Y}")

# ---- Filters (left sidebar) ----
st.sidebar.header("Filters")
segments = st.sidebar.multiselect(
    "Segment", sorted(accounts["segment"].unique()), default=sorted(accounts["segment"].unique()))
contract_types = st.sidebar.multiselect(
    "Contract type", sorted(accounts["contract_type"].unique()), default=sorted(accounts["contract_type"].unique()))
renewal_window = st.sidebar.slider("Renewing within (days)", 0, 365, 365, step=15)

shown = accounts[
    accounts["segment"].isin(segments)
    & accounts["contract_type"].isin(contract_types)
    & (accounts["days_to_renewal"] <= renewal_window)
]

# ---- Headline numbers ----
renewing_soon = shown[shown["days_to_renewal"] <= 90]
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Accounts", len(shown))
col2.metric("Total ARR", f"${shown['arr_usd'].sum() / 1_000_000:.1f}M")
col3.metric("Renewals ≤ 90d", len(renewing_soon))
col4.metric("ARR renewing ≤ 90d", f"${renewing_soon['arr_usd'].sum() / 1_000_000:.1f}M")
col5.metric("Sponsor not engaged", int((shown["sponsor_status"] != "Engaged").sum()))

# ---- Account table ----
st.subheader("Accounts")
st.dataframe(
    shown.sort_values("days_to_renewal"),
    hide_index=True,
    use_container_width=True,
    column_order=[
        "account_name", "segment", "contract_type", "arr_usd", "days_to_renewal",
        "seat_use_pct", "usage_vs_commit_pct", "usage_trend_90d_pct",
        "open_tickets", "sev1_tickets_90d", "sponsor_status", "days_since_sponsor_call",
        "last_survey_score", "csm_note",
    ],
    column_config={
        "account_name": "Account",
        "segment": "Segment",
        "contract_type": "Contract",
        "arr_usd": st.column_config.NumberColumn("ARR", format="dollar"),
        "days_to_renewal": st.column_config.NumberColumn("Days to renewal"),
        "seat_use_pct": st.column_config.NumberColumn("Seats used", format="%d%%"),
        "usage_vs_commit_pct": st.column_config.NumberColumn("Usage vs commit", format="%d%%"),
        "usage_trend_90d_pct": st.column_config.NumberColumn("Usage trend (90d)", format="%+d%%"),
        "open_tickets": "Open tickets",
        "sev1_tickets_90d": "Sev-1 (90d)",
        "sponsor_status": "Sponsor",
        "days_since_sponsor_call": st.column_config.NumberColumn("Days since sponsor call"),
        "last_survey_score": st.column_config.NumberColumn("Survey (0-10)"),
        "csm_note": st.column_config.TextColumn("CSM note", width="large"),
    },
)
st.caption("Blank seat or usage cells mean that measure isn't part of the account's contract.")
