import os
import pandas as pd
import yfinance as yf
import requests
from io import StringIO
import streamlit as st


DATA_DIR = "data"
FALLBACK_FILE = os.path.join(DATA_DIR, "nifty500_fallback.csv")

os.makedirs(DATA_DIR, exist_ok=True)


@st.cache_data(ttl=86400)
def get_nifty_500_symbols():
    """
    Try fetching live NIFTY 500 symbols. If it fails, use fallback CSV.
    """
    try:
        st.write("📥 Fetching NIFTY 500 list from NSE...")
        url = "https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.nseindia.com/"
        }

        session = requests.Session()
        session.headers.update(headers)
        session.get("https://www.nseindia.com", timeout=5)

        response = session.get(url, timeout=10)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        symbols = df['Symbol'].tolist()
        st.success(f"✅ Loaded {len(symbols)} NIFTY 500 symbols (live).")

        # Save fallback
        df.to_csv(FALLBACK_FILE, index=False)

        return symbols

    except Exception as e:
        st.warning(f"⚠️ Failed to fetch live data: {e}")

        if os.path.exists(FALLBACK_FILE):
            st.info("📂 Using fallback NIFTY 500 CSV from data directory.")
            df = pd.read_csv(FALLBACK_FILE)
            return df['Symbol'].tolist()

        # Ask user to upload file
        uploaded_file = st.file_uploader(
            "📤 Upload a NIFTY 500 CSV file (must include 'Symbol' column):",
            type=["csv"]
        )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            if "Symbol" not in df.columns:
                st.error("❌ Uploaded file does not contain 'Symbol' column.")
                return []
            df.to_csv(FALLBACK_FILE, index=False)
            st.success("✅ File uploaded and saved. Using it now.")
            return df["Symbol"].tolist()

        st.stop()


@st.cache_data(ttl=3600)
def get_top_50_stocks():
    symbols = get_nifty_500_symbols()

    if not symbols:
        st.warning("⚠️ No symbols to process.")
        return pd.DataFrame()

    st.write(f"🔍 Processing {len(symbols)} stocks...")

    all_data = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.info

            if not all(k in info for k in ['trailingPE', 'marketCap', 'trailingEps']):
                continue

            pe = info.get("trailingPE", 0)
            roe = info.get("returnOnEquity", 0)
            eps = info.get("trailingEps", 0)

            if (
                info.get("marketCap", 0) > 1e10 and
                0 < pe < 40 and
                eps > 0 and
                roe and roe > 0.10
            ):
                all_data.append({
                    "Symbol": symbol,
                    "Name": info.get("shortName", ""),
                    "Market Cap": info.get("marketCap", 0),
                    "PE Ratio": pe,
                    "ROE": f"{roe * 100:.2f}%",
                    "EPS": eps,
                    "Dividend Yield": f"{(info.get('dividendYield') or 0) * 100:.2f}%",
                    "Sector": info.get("sector", "")
                })

        except Exception as e:
            st.write(f"❌ Error fetching {symbol}: {e}")
            continue

    if not all_data:
        st.warning("⚠️ No fundamentally strong stocks found.")
        return pd.DataFrame()

    df = pd.DataFrame(all_data)
    df = df.sort_values(by="Market Cap", ascending=False).head(50).reset_index(drop=True)
    st.success(f"✅ Found {len(df)} top fundamentally strong stocks.")
    return df
