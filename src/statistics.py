import numpy as np
import pandas as pd

def calculate_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna()

def historical_mean(returns: pd.DataFrame) -> pd.Series:
    return returns.mean()

def covariance_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.cov()