import pandas as pd
import requests
from io import StringIO

def get_nifty_500_symbols():
    """
    Fetches the latest list of NIFTY 500 stock symbols from NSE India.
    Returns a list of stock symbols.
    """
    try:
        # URL to the NIFTY 500 constituents CSV
        csv_url = "https://www.nseindia.com/content/indices/ind_nifty500list.csv"

        # Set headers to mimic a browser visit
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.nseindia.com/"
        }

        # Create a session to handle cookies and headers
        session = requests.Session()
        session.headers.update(headers)

        # Make an initial request to establish the session
        session.get("https://www.nseindia.com", timeout=5)

        # Fetch the CSV file
        response = session.get(csv_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Read the CSV content
        df = pd.read_csv(StringIO(response.text))

        # Extract the 'Symbol' column and return as a list
        symbols = df['Symbol'].tolist()
        return symbols

    except Exception as e:
        print(f"Error fetching NIFTY 500 symbols: {e}")
        return []
