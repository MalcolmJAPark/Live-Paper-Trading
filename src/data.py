#!/usr/bin/env python3
# data.py

import sqlite3
import pandas as pd
import yfinance as yf
import datetime
import time
import schedule  # pip install schedule

DB_PATH     = 'prices.db'
PRICE_TABLE = 'prices'
BS_TABLE    = 'balance_sheets'

def fetch_sp500_tickers():
    """
    Scrape the current list of S&P 500 companies from Wikipedia.
    Returns a list of ticker strings (with '.' → '-' for Yahoo compatibility).
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url, header=0)[0]
    return [t.replace('.', '-') for t in table['Symbol'].tolist()]

def get_prices(tickers, start, end, db_path=DB_PATH, table_name=PRICE_TABLE):
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

def get_balance_sheet(ticker, db_path=DB_PATH, table_name=BS_TABLE):
    tk = yf.Ticker(ticker)
    bs = tk.balance_sheet
    if bs.empty:
        raise ValueError(f"No balance sheet data for {ticker!r}")

    latest = bs.columns.max()
    try:
        book_value = bs.loc['Stockholders Equity', latest]
    except KeyError:
        raise KeyError("Missing 'Stockholders Equity' row")

    info   = tk.info
    shares = info.get('sharesOutstanding')
    price  = info.get('regularMarketPrice') or info.get('currentPrice')
    if not shares or not price:
        raise KeyError("Couldn’t get sharesOutstanding or price")

    btm = (book_value / shares) / price

    df = pd.DataFrame([{
        'Date': latest,
        'Ticker': ticker,
        'BookValue': book_value,
        'SharesOutstanding': shares,
        'CurrentPrice': price,
        'BookToMarket': btm
    }])

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    return df

def daily_update():
    today     = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tickers   = fetch_sp500_tickers()

    print(f"[{datetime.datetime.now()}] Fetching prices for {len(tickers)} S&P 500 tickers…")
    get_prices(tickers, start=yesterday, end=today)

    for t in tickers:
        try:
            get_balance_sheet(t)
        except Exception as e:
            print(f"[{t}] SKIPPED ({e})")

    print(f"[{datetime.datetime.now()}] Done.\n")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        daily_update()
    else:
        # schedule daily at 18:00 local time
        schedule.every().day.at("19:35").do(daily_update)
        print("Scheduler started. CTRL-C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(60)
