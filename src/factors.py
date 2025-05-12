import pandas as pd

__all__ = [
    "size_factor",
    "value_factor",
    "momentum_factor",
    "quality_factor",
    "low_vol_factor",
]

def size_factor(df: pd.DataFrame) -> pd.Series:
    """
    Dummy Size factor: returns zeros for each entry in df.
    """
    return pd.Series(0.0, index=df.index, name="size_factor")

def value_factor(df: pd.DataFrame) -> pd.Series:
    """
    Dummy Value factor: returns zeros for each entry in df.
    """
    return pd.Series(0.0, index=df.index, name="value_factor")

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
