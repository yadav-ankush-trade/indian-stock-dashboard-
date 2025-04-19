import streamlit as st
import pandas as pd
from utils.stock_utils import get_top_50_stocks

st.set_page_config(page_title="Top 50 Indian Stocks", layout="wide")

st.title("🏆 Top 50 Fundamentally Strong Indian Stocks")

df = get_top_50_stocks()

st.dataframe(df, use_container_width=True)
