import numpy as np
import pandas as pd

def portfolio_volatility(portfolio_returns: pd.Series) -> float:
    return portfolio_returns.std() * np.sqrt(252)

def portfolio_sharpe(portfolio_returns: pd.Series, risk_free_rate=0.0) -> float:
    excess_return = portfolio_returns - risk_free_rate / 252
    return excess_return.mean() / excess_return.std() * np.sqrt(252)

def max_drawdown(portfolio_cum_returns: pd.Series) -> float:
    roll_max = portfolio_cum_returns.cummax()
    drawdown = (portfolio_cum_returns - roll_max) / roll_max
    return drawdown.min()

def var_historical(portfolio_returns: pd.Series, confidence_level=0.05) -> float:
    return np.percentile(portfolio_returns, 100 * confidence_level)

def cvar_historical(portfolio_returns: pd.Series, confidence_level=0.05) -> float:
    var = var_historical(portfolio_returns, confidence_level)
    return portfolio_returns[portfolio_returns <= var].mean()