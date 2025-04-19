import pandas as pd
import yfinance as yf
import requests
from io import StringIO
import streamlit as st


@st.cache_data(ttl=86400)
def get_nifty_500_symbols():
    """
    Fetch the latest NIFTY 500 symbols from NSE website.
    Returns list of symbols (e.g., ['RELIANCE', 'INFY', ...])
    """
    try:
        url = "https://www.nseindia.com/content/indices/ind_nifty500list.csv"
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
        return df['Symbol'].tolist()

    except Exception as e:
        print(f"Failed to fetch NIFTY 500 symbols: {e}")
        return []


@st.cache_data(ttl=3600)
def get_top_50_stocks():
    """
    Filters top 50 fundamentally strong stocks from NIFTY 500.
    """
    symbols = get_nifty_500_symbols()
    all_data = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.info

            # Check required fields
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

        except Exception:
            continue

    df = pd.DataFrame(all_data)
    return df.sort_values("Market Cap", ascending=False).head(50).reset_index(drop=True)
