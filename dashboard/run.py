import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests

from streamlit_autorefresh import st_autorefresh
from app.services.mt5_service import (
    get_account_info,
    get_open_positions,
    get_symbol_price,
    open_trade,
    close_trade,
)

API_URL = "http://localhost:8000/trades/history"

# Configure dashboard
st.set_page_config(page_title="Trading Dashboard", layout="wide")
st.title("Trading Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
refresh_rate = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
symbol = st.sidebar.selectbox("Select symbol", ["EURUSD", "GBPUSD", "XAUUSD", "USDJPY"])
lot_size = st.sidebar.number_input("Lot size", min_value=0.01, value=0.1, step=0.01)

# Trade buttons
if st.sidebar.button("BUY"):
    result = open_trade(symbol, lot_size, "BUY")
    st.sidebar.write(result)

if st.sidebar.button("SELL"):
    result = open_trade(symbol, lot_size, "SELL")
    st.sidebar.write(result)

# Auto-refresh
count = st_autorefresh(interval=refresh_rate * 1000, limit=None, key="refresh")

# Persist account history
if "account_history" not in st.session_state:
    st.session_state.account_history = []

# Account info
try:
    account_info = get_account_info()
    if account_info:
        st.subheader("Account Info")
        st.json(account_info)

        st.session_state.account_history.append({
            "time": datetime.datetime.now(),
            "equity": account_info.get("equity", 0),
            "balance": account_info.get("balance", 0),
            "profit": account_info.get("profit", 0),
        })
except Exception as e:
    st.error(f"Error fetching account info: {e}")

# Equity curve chart
if st.session_state.account_history:
    df = pd.DataFrame(st.session_state.account_history)
    fig = px.line(df, x="time", y=["equity", "balance", "profit"],
                  title="Account Performance Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Live price
st.subheader(f"Live Price: {symbol}")
price = get_symbol_price(symbol)
if price:
    st.json(price)

# Positions with close buttons
st.subheader("Open Positions")
positions = get_open_positions(symbol)
if positions:
    df_pos = pd.DataFrame(positions)
    st.dataframe(df_pos)

    for pos in positions:
        if st.button(f"Close {pos['ticket']} ({pos['symbol']} {pos['type']})"):
            result = close_trade(pos["ticket"])
            st.write(result)
else:
    st.info("No open positions.")

# Trade history table
st.subheader("Trade History")
try:
    resp = requests.get(API_URL)
    data = resp.json()
    if data["status"] == "success":
        trades = data["data"]
        if trades:
            df_hist = pd.DataFrame(trades)
            st.dataframe(df_hist)
            # Optional: cumulative profit chart
            df_hist["cumulative_profit"] = df_hist["profit"].cumsum()
            fig_hist = px.line(df_hist, x="created_at", y="cumulative_profit",
                               title="Cumulative Profit Over Time")
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No trades logged yet.")
    else:
        st.error(f"Error: {data.get('message', 'Unknown error')}")
except Exception as e:
    st.error(f"Failed to fetch trades: {e}")
