import streamlit as st
import pandas as pd
from utils.stock_utils import get_nifty_500_symbols



st.set_page_config(page_title="Top 500 Indian Stocks", layout="wide")

st.title("🏆 Top 50 Fundamentally Strong Indian Stocks")

df = get_nifty_500_symbols()

st.dataframe(df, use_container_width=True)
