import yfinance as yf

# pick any ticker
t = yf.Ticker("AAPL")

# fetch its annual balance sheet
bs = t.balance_sheet

# list all the line‐items (features)
print("Balance sheet fields:\n", bs.index.tolist())

# list all the reporting dates (periods)
print("Reporting dates:\n", bs.columns.tolist())
