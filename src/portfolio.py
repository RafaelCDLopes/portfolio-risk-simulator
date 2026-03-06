import numpy as np
import pandas as pd

def portfolio_return(returns: pd.DataFrame, weights: np.array) -> pd.Series:
    if len(weights) != returns.shape[1]:
        raise ValueError("O número de pesos deve corresponder ao número de ativos.")
    return returns.dot(weights)

def cumulative_return(portfolio_returns: pd.Series) -> pd.Series:
    return (1 + portfolio_returns).cumprod()