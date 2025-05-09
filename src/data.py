import sqlite3
import pandas as pd
import yfinance as yf

def get_prices(tickers, start, end, db_path='prices.db', table_name='prices'):
    """
    Download historical price data for given ticker(s) between start and end dates,
    and write the data to a local SQLite database.
    """
    data = yf.download(tickers=tickers, start=start, end=end, progress=False)
    if isinstance(tickers, (list, tuple)):
        df = (
            data
            .stack(level=1)
            .rename_axis(('Date', 'Ticker'))
            .reset_index()
        )
    else:
        df = data.reset_index()
        df.insert(1, 'Ticker', tickers)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    return df

def get_balance_sheet(ticker, db_path='prices.db', table_name='balance_sheets'):
    """
    Download the latest balance sheet for a given ticker,
    extract book value and shares outstanding, compute book-to-market ratio,
    and append the result to a SQLite table.

    Args:
        ticker (str): Stock symbol, e.g. 'AAPL'
        db_path (str): Path to your SQLite .db file (default: 'prices.db')
        table_name (str): Name of the SQLite table (default: 'balance_sheets')

    Returns:
        pandas.DataFrame: one-row DataFrame with:
          Date, Ticker, BookValue, SharesOutstanding,
          CurrentPrice, BookToMarket
    """
    # 1. Fetch balance sheet DataFrame
    tk = yf.Ticker(ticker)
    bs = tk.balance_sheet
    if bs.empty:
        raise ValueError(f"No balance sheet data found for {ticker!r}")

    # 2. Pick the latest period
    latest = bs.columns.max()

    # 3. Extract book value (Total Stockholder Equity)
    try:
        book_value = bs.loc['Total Stockholder Equity', latest]
    except KeyError:
        raise KeyError("Could not find 'Total Stockholder Equity' in balance sheet")

    # 4. Get shares outstanding & price from Ticker.info
    info = tk.info
    shares = info.get('sharesOutstanding')
    if shares is None:
        raise KeyError("Could not find 'sharesOutstanding' in ticker.info")
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    if price is None:
        raise KeyError("Could not find current market price in ticker.info")

    # 5. Compute book-to-market ratio
    btm = (book_value / shares) / price

    # 6. Build a one-row DataFrame
    df = pd.DataFrame([{
        'Date': latest,
        'Ticker': ticker,
        'BookValue': book_value,
        'SharesOutstanding': shares,
        'CurrentPrice': price,
        'BookToMarket': btm
    }])

    # 7. Append to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()

    return df
