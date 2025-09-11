# -*- coding: utf-8 -*-
# Stock Peer Analysis Dashboard (Fixed Version)

import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Stock peer analysis dashboard",
    page_icon="📈",
    layout="wide",
)

"""
# 📊 Stock Peer Analysis

Easily compare stocks against others in their peer group.
"""

# -----------------------------------------------------
# Utility functions
# -----------------------------------------------------
def stocks_to_str(stocks):
    return ",".join(stocks)


def get_query_stocks():
    """Get stocks from query params, or fall back to defaults."""
    query_params = st.experimental_get_query_params()
    if "stocks" in query_params:
        return query_params["stocks"][0].split(",")
    return DEFAULT_STOCKS


def set_query_stocks(stocks):
    if stocks:
        st.experimental_set_query_params(stocks=stocks_to_str(stocks))
    else:
        st.experimental_set_query_params()


# -----------------------------------------------------
# Stock lists
# -----------------------------------------------------
STOCKS = [
    "AAPL","ABBV","ACN","ADBE","ADP","AMD","AMGN","AMT","AMZN","APD","AVGO",
    "AXP","BA","BK","BKNG","BMY","BRK.B","BSX","C","CAT","CI","CL","CMCSA",
    "COST","CRM","CSCO","CVX","DE","DHR","DIS","DUK","ELV","EOG","EQR","FDX",
    "GD","GE","GILD","GOOG","GOOGL","HD","HON","HUM","IBM","ICE","INTC","ISRG",
    "JNJ","JPM","KO","LIN","LLY","LMT","LOW","MA","MCD","MDLZ","META","MMC",
    "MO","MRK","MSFT","NEE","NFLX","NKE","NOW","NVDA","ORCL","PEP","PFE","PG",
    "PLD","PM","PSA","REGN","RTX","SBUX","SCHW","SLB","SO","SPGI","T","TJX",
    "TMO","TSLA","TXN","UNH","UNP","UPS","V","VZ","WFC","WM","WMT","XOM",
]
DEFAULT_STOCKS = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA", "META"]

# -----------------------------------------------------
# Layout
# -----------------------------------------------------
cols = st.columns([1, 3])
top_left_cell = cols[0].container(border=True, height="stretch", vertical_alignment="center")

# -----------------------------------------------------
# Inputs
# -----------------------------------------------------
with top_left_cell:
    tickers = st.multiselect(
        "Stock tickers",
        options=sorted(set(STOCKS) | set(get_query_stocks())),
        default=get_query_stocks(),
        placeholder="Choose stocks to compare. Example: NVDA",
    )

horizon_map = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y",
    "20 Years": "20y",
}

with top_left_cell:
    horizon = st.radio(
        "Time horizon",
        options=list(horizon_map.keys()),
        index=2,  # default = "6 Months"
        horizontal=True,
    )

tickers = [t.upper() for t in tickers]
set_query_stocks(tickers)

if not tickers:
    top_left_cell.info("Pick some stocks to compare", icon="ℹ️")
    st.stop()

right_cell = cols[1].container(border=True, height="stretch", vertical_alignment="center")

# -----------------------------------------------------
# Data loading
# -----------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_data(tickers, period):
    tickers_obj = yf.Tickers(" ".join(tickers))
    data = tickers_obj.history(period=period)
    if data is None or data.empty:
        raise RuntimeError("YFinance returned no data.")
    return data["Close"]

try:
    data = load_data(tickers, horizon_map[horizon])
except yf.exceptions.YFRateLimitError:
    st.warning("YFinance is rate-limiting us 😕. Try again later.")
    load_data.clear()
    st.stop()

empty_columns = data.columns[data.isna().all()].tolist()
if empty_columns:
    st.error(f"Error loading data for: {', '.join(empty_columns)}.")
    st.stop()

# -----------------------------------------------------
# Normalize prices
# -----------------------------------------------------
normalized = data.div(data.iloc[0])
latest_norm_values = {normalized[ticker].iat[-1]: ticker for ticker in tickers}
max_norm_value = max(latest_norm_values.items())
min_norm_value = min(latest_norm_values.items())

# -----------------------------------------------------
# Best/Worst Stocks
# -----------------------------------------------------
bottom_left_cell = cols[0].container(border=True, height="stretch", vertical_alignment="center")
with bottom_left_cell:
    cols2 = st.columns(2)
    cols2[0].metric(
        "Best stock",
        max_norm_value[1],
        delta=f"{round((max_norm_value[0]-1) * 100)}%",
    )
    cols2[1].metric(
        "Worst stock",
        min_norm_value[1],
        delta=f"{round((min_norm_value[0]-1) * 100)}%",
    )

# -----------------------------------------------------
# Normalized Prices Chart
# -----------------------------------------------------
with right_cell:
    st.altair_chart(
        alt.Chart(
            normalized.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized price"
            )
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized price:Q").scale(zero=False),
            alt.Color("Stock:N"),
        )
        .properties(height=400),
        use_container_width=True,
    )

# -----------------------------------------------------
# Peer Average Comparison
# -----------------------------------------------------
"""
## Individual stocks vs peer average

For the analysis below, the "peer average" when analyzing stock X always
excludes X itself.
"""

if len(tickers) <= 1:
    st.warning("Pick 2 or more tickers to compare them")
    st.stop()

NUM_COLS = 4
cols = st.columns(NUM_COLS)

for i, ticker in enumerate(tickers):
    peers = normalized.drop(columns=[ticker])
    peer_avg = peers.mean(axis=1)

    # Stock vs Peer Average
    plot_data = pd.DataFrame(
        {"Date": normalized.index, ticker: normalized[ticker], "Peer average": peer_avg}
    ).melt(id_vars=["Date"], var_name="Series", value_name="Price")

    chart = (
        alt.Chart(plot_data)
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Price:Q").scale(zero=False),
            alt.Color("Series:N", scale=alt.Scale(domain=[ticker, "Peer average"], range=["red", "gray"])),
            alt.Tooltip(["Date", "Series", "Price"]),
        )
        .properties(title=f"{ticker} vs peer average", height=300)
    )

    cell = cols[(i * 2) % NUM_COLS].container(border=True)
    cell.altair_chart(chart, use_container_width=True)

    # Delta vs Peer
    plot_data = pd.DataFrame(
        {"Date": normalized.index, "Delta": normalized[ticker] - peer_avg}
    )

    chart = (
        alt.Chart(plot_data)
        .mark_area()
        .encode(alt.X("Date:T"), alt.Y("Delta:Q").scale(zero=False))
        .properties(title=f"{ticker} minus peer average", height=300)
    )

    cell = cols[(i * 2 + 1) % NUM_COLS].container(border=True)
    cell.altair_chart(chart, use_container_width=True)

# -----------------------------------------------------
# Raw Data
# -----------------------------------------------------
"""
## Raw data
"""
st.dataframe(data)
