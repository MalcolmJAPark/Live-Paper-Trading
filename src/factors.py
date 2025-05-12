import pandas as pd
import numpy as np
import sqlite3

__all__ = [
    "size_factor",
    "value_factor",
    "momentum_factor",
    "quality_factor",
    "low_vol_factor",
]

def size_factor(df: pd.DataFrame) -> pd.Series:
    """
    Size factor: log of market capitalization (CurrentPrice × SharesOutstanding).
    """
    market_cap = df["CurrentPrice"] * df["SharesOutstanding"]
    size = np.log(market_cap.replace({0: np.nan}))
    return pd.Series(size, index=df.index, name="size_factor")


def value_factor(df: pd.DataFrame) -> pd.Series:
    """
    Value factor: book-to-market ratio (BookToMarket column).
    """
    val = df["BookToMarket"]
    return pd.Series(val, index=df.index, name="value_factor")


def momentum_factor(df: pd.DataFrame) -> pd.Series:
    """
    Dummy Momentum factor: returns zeros for each entry in df.
    """
    return pd.Series(0.0, index=df.index, name="momentum_factor")


def quality_factor(df: pd.DataFrame) -> pd.Series:
    """
    Dummy Quality factor: returns zeros for each entry in df.
    """
    return pd.Series(0.0, index=df.index, name="quality_factor")


def low_vol_factor(df: pd.DataFrame) -> pd.Series:
    """
    Dummy Low Volatility factor: returns zeros for each entry in df.
    """
    return pd.Series(0.0, index=df.index, name="low_vol_factor")


if __name__ == "__main__":
    # Example usage: load balance_sheets from SQLite DB 'prices.db'
    conn = sqlite3.connect("prices.db")
    df = pd.read_sql(
        "SELECT * FROM balance_sheets", conn,
        parse_dates=["Date"]
    )
    # Set MultiIndex (Date, Ticker)
    df.set_index(["Date", "Ticker"], inplace=True)

    # Compute factors
    df["size_factor"] = size_factor(df)
    df["value_factor"] = value_factor(df)

    # Inspect first rows of daily factor DataFrame
    print(df[["size_factor", "value_factor"]].head())
    conn.close()