import streamlit as st
from utils.stock_utils import get_top_50_stocks

st.set_page_config(page_title="Top 50 Indian Stocks", layout="wide")

st.title("📈 Top 50 Fundamentally Strong Indian Stocks")

with st.spinner("Loading data..."):
    df = get_top_50_stocks()

if df.empty:
    st.error("⚠️ No stock data available. Please try again later.")
else:
    st.dataframe(df, use_container_width=True)
