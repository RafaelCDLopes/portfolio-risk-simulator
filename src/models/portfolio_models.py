import numpy as np
import pandas as pd

class PortfolioModel:
    def __init__(self, prices: pd.DataFrame, weights: np.array):
        self.prices = prices
        self.weights = weights

        self.returns = self._compute_returns()
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov()

    def _compute_returns(self):
        return self.prices.pct_change().dropna()

    def portfolio_returns(self):
        return self.returns.dot(self.weights)

    def cumulative_returns(self):
        port_ret = self.portfolio_returns()
        return (1 + port_ret).cumprod()

    def volatility(self):
        return np.sqrt(self.weights.T @ self.cov_matrix @ self.weights)

    def expected_return(self):
        return np.sum(self.mean_returns * self.weights)

    def sharpe_ratio(self, risk_free_rate=0.0):
        vol = self.volatility()
        if vol == 0:
            return np.nan
        return (self.expected_return() - risk_free_rate) / vol

    def max_drawdown(self):
        cum = self.cumulative_returns()
        peak = cum.cummax()
        drawdown = (cum - peak) / peak

        return drawdown.min()

    def var(self, alpha=0.05):
        port_ret = self.portfolio_returns()
        return np.percentile(port_ret, alpha * 100)

    def cvar(self, alpha=0.05):
        port_ret = self.portfolio_returns()
        var = self.var(alpha)
        return port_ret[port_ret <= var].mean()