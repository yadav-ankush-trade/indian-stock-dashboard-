import pandas as pd

def get_top_50_stocks():
    # Option 1: Load from CSV (pre-filtered)
    return pd.read_csv("data/top_50_stocks.csv")

    # Option 2: OR fetch live data and apply your filtering logic:
    # - Large market cap
    # - Positive ROE
    # - Low PE
    # (this is a placeholder, as pulling and filtering live data for 500+ stocks would need NSE/BSE API access)
