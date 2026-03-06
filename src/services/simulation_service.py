import numpy as np
import pandas as pd
from src.utils.finance_utils import compute_returns

class MonteCarloService:
    @staticmethod
    def simulate(prices, weights, simulations=1000):
        returns = compute_returns(prices)
        mean = returns.mean().values
        cov = returns.cov().values
        days = len(returns)

        # Vectorized Monte Carlo simulation to evitar loops pesados em Python
        rand_returns = np.random.multivariate_normal(mean, cov, (simulations, days))
        # rand_returns: (simulations, days, n_assets)
        port_returns = rand_returns @ weights  # (simulations, days)
        sims = (1 + port_returns).cumprod(axis=1).T  # (days, simulations)

        return pd.DataFrame(sims)