import numpy as np
import pandas as pd

def monte_carlo_simulation(weights, mean_returns, cov_matrix, num_days=252, num_simulations=1000):
    results = []
    for _ in range(num_simulations):
        simulated_returns = np.random.multivariate_normal(mean_returns, cov_matrix, num_days)
        portfolio_returns = simulated_returns.dot(weights)
        cumulative = np.cumprod(1 + portfolio_returns)
        results.append(cumulative)
    return np.array(results)