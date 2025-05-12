from data import get_balance_sheet

# this will append a row to `prices.db` → table `balance_sheets`
df = get_balance_sheet('NVDA')
print(df)