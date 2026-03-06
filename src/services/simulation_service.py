import numpy as np
import pandas as pd

class MonteCarloService:
    @staticmethod
    def simulate(prices, weights, simulations=1000):
        returns = prices.pct_change().dropna()
        mean = returns.mean().values
        cov = returns.cov().values
        days = len(returns)

        # Vectorized Monte Carlo simulation to evitar loops pesados em Python
        rand_returns = np.random.multivariate_normal(mean, cov, (simulations, days))
        # rand_returns: (simulations, days, n_assets)
        port_returns = rand_returns @ weights  # (simulations, days)
        sims = (1 + port_returns).cumprod(axis=1).T  # (days, simulations)

        return pd.DataFrame(sims)