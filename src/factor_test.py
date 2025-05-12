#!/usr/bin/env python3
import sqlite3
import pandas as pd
from factors import (
    size_factor,
    value_factor,
    momentum_factor,
    quality_factor,
    low_vol_factor,
)

# 1. Connect & list your tables so you know the exact name
conn = sqlite3.connect("prices.db")
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';", conn
)
print("Tables in prices.db:", tables["name"].tolist())

# 2. Read your price table (replace `prices` with whatever you see above)
df = pd.read_sql(
    "SELECT * FROM balance_sheets",  # <-- change this to your table name
    conn,
    parse_dates=["Date"],
)

print(f"Loaded {len(df)} rows.")

# 3. Wire up & run each stub
stubs = [size_factor, value_factor, momentum_factor, quality_factor, low_vol_factor]
for fn in stubs:
    col = fn(df)
    # 4a. Attach to DataFrame so you can inspect
    df[fn.__name__] = col
    # 4b. Quick check that it’s all zeros
    assert (col == 0.0).all(), f"{fn.__name__!r} did not return all zeros!"

print("All factor stubs returned zero-series of correct length.")
print("Columns now include:", [fn.__name__ for fn in stubs])
print(df.tail())