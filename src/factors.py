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
    Momentum factor: 252- to 21-day total return.
    Skips stocks with fewer than 252 trading days (yields NaN).
    """
    # Use groupby.transform to align with the original DataFrame index, handling duplicates
    mom = (
        df["CurrentPrice"]
        .groupby(level="Ticker")
        .transform(lambda s: s.shift(21) / s.shift(252) - 1)
    )
    return pd.Series(mom, index=df.index, name="momentum_factor")


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
    # Load balance_sheets from SQLite DB 'prices.db'
    conn = sqlite3.connect("prices.db")
    df = pd.read_sql(
        "SELECT * FROM balance_sheets", conn,
        parse_dates=["Date"]
    )
    df.set_index(["Date", "Ticker"], inplace=True)

    # Compute factors
    df["size_factor"] = size_factor(df)
    df["value_factor"] = value_factor(df)
    df["momentum_factor"] = momentum_factor(df)

    # Inspect first rows of daily factor DataFrame
    print(df[["size_factor", "value_factor", "momentum_factor"]].head())
    conn.close()
