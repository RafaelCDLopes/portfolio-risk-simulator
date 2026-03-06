from __future__ import annotations
import pandas as pd

_DASH_EQUIVALENTS = ("\u2013", "\u2014", "\u2212", "\u2010", "\u2011")

def normalize_ticker(ticker: str) -> str:
    """Normaliza ticker (ex: BTC–USD -> BTC-USD)."""
    if not isinstance(ticker, str):
        ticker = str(ticker)
    for char in _DASH_EQUIVALENTS:
        ticker = ticker.replace(char, "-")
    return ticker.strip()

def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Retornos simples a partir de preços."""
    return prices.pct_change().dropna()

