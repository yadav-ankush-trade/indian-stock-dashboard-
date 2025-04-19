import streamlit as st
import yfinance as yf
from utils.stock_utils import get_nifty_500_symbols

st.set_page_config(page_title="Stock Details", layout="centered")
st.title("📊 Stock Details Viewer")

symbols = get_nifty_500_symbols()

if not symbols:
    st.error("⚠️ Could not load NIFTY 500 stock list.")
else:
    selected_stock = st.selectbox("Choose a stock to view details:", sorted(symbols))

    if selected_stock:
        with st.spinner("Fetching stock data..."):
            try:
                ticker = yf.Ticker(selected_stock + ".NS")
                info = ticker.info

                st.subheader(f"{info.get('longName', selected_stock)} ({selected_stock}.NS)")
                st.metric("Current Price", f"₹ {info.get('regularMarketPrice', 'N/A')}")
                st.write("### Summary")
                st.write(info.get("longBusinessSummary", "No summary available."))

                st.write("### Key Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Market Cap:** ₹ {info.get('marketCap', 0):,}")
                    st.write(f"**PE Ratio (TTM):** {info.get('trailingPE', 'N/A')}")
                    st.write(f"**EPS (TTM):** {info.get('trailingEps', 'N/A')}")
                    st.write(f"**52 Week High:** ₹ {info.get('fiftyTwoWeekHigh', 'N/A')}")
                with col2:
                    st.write(f"**Dividend Yield:** {info.get('dividendYield', 0) * 100:.2f}%")
                    st.write(f"**52 Week Low:** ₹ {info.get('fiftyTwoWeekLow', 'N/A')}")
                    st.write(f"**Volume:** {info.get('volume', 'N/A'):,}")
                    st.write(f"**Beta:** {info.get('beta', 'N/A')}")

            except Exception as e:
                st.error(f"⚠️ Failed to fetch data for {selected_stock}: {e}")
