import numpy as np
import pandas as pd

class MonteCarloService:
    @staticmethod
    def simulate(prices, weights, simulations=1000):
        returns = prices.pct_change().dropna()
        mean = returns.mean().values
        cov = returns.cov().values
        days = len(returns)
        sims = np.zeros((days, simulations))

        for i in range(simulations):
            rand_returns = np.random.multivariate_normal(mean, cov, days)
            port_returns = rand_returns @ weights
            sims[:, i] = (1 + port_returns).cumprod()

        return pd.DataFrame(sims)