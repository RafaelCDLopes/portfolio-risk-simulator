import numpy as np
import pandas as pd
from src.utils.finance_utils import compute_returns

class PortfolioModel:
    def __init__(self, prices: pd.DataFrame, weights: np.array):
        self.prices = prices
        self.weights = weights

        self.returns = PortfolioModel.returns(self.prices)
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov()

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

    def efficient_frontier(self, n_portfolios: int = 3000, risk_free_rate: float = 0.0):
        n_assets = len(self.weights)
        results = np.zeros((n_portfolios, 3))  # [vol, ret, sharpe]
        weights_record = np.zeros((n_portfolios, n_assets))

        cov = self.cov_matrix.values
        mean = self.mean_returns.values

        for i in range(n_portfolios):
            w = np.random.random(n_assets)
            w /= w.sum()
            weights_record[i, :] = w

            port_ret = np.sum(mean * w)
            port_vol = np.sqrt(w.T @ (cov @ w))
            sharpe = (port_ret - risk_free_rate) / port_vol if port_vol > 0 else np.nan

            results[i] = np.array([port_vol, port_ret, sharpe])

        max_sharpe_idx = np.nanargmax(results[:, 2])
        opt_weights = weights_record[max_sharpe_idx]
        opt_metrics = {
            "Expected Return": results[max_sharpe_idx, 1],
            "Volatility": results[max_sharpe_idx, 0],
            "Sharpe": results[max_sharpe_idx, 2],
        }

        return results, opt_weights, opt_metrics

    @staticmethod
    def returns(prices: pd.DataFrame):
        return compute_returns(prices)

    @staticmethod
    def correlation_matrix(returns: pd.DataFrame):
        return returns.corr()