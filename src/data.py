import sqlite3
import pandas as pd
import yfinance as yf

def get_prices(tickers, start, end, db_path='prices.db', table_name='prices'):
    """
    Download historical price data for given ticker(s) between start and end dates,
    and write the data to a local SQLite database.

    Args:
        tickers (str or list of str): A single ticker symbol or list of symbols.
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).
        db_path (str): Path to the SQLite .db file.
        table_name (str): Name of the table into which to write the data.
    """
    # 1. Download data
    data = yf.download(tickers=tickers, start=start, end=end, progress=False)

    # 2. Normalize into a flat table
    if isinstance(tickers, (list, tuple)):
        # Multi-ticker: columns are a MultiIndex [field, ticker]
        df = data.stack(level=1).rename_axis(('Date', 'Ticker')).reset_index()
    else:
        # Single-ticker: simple DataFrame
        df = data.reset_index()
        df.insert(1, 'Ticker', tickers)

    # 3. Write to SQLite
    conn = sqlite3.connect(db_path)                  # creates file if needed
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
