import numpy as np
import streamlit as st
from src.services.data_loader import DataLoader
from src.views.portfolio_view import PortfolioView
from src.models.portfolio_models import PortfolioModel

class PortfolioController:
    def run(self):
        tickers, start, end, simulations, frequency = PortfolioView.input_section()
        weights = PortfolioView.weight_section(tickers)
        run = PortfolioView.run_button()

        if not run:
            return

        if sum(weights) == 0:
            return

        weights = np.array(weights) / sum(weights)
        prices = DataLoader.load_prices(tickers, start, end, frequency=frequency)

        valid_tickers = list(prices.columns)
        weights = np.array([weights[tickers.index(t)] for t in valid_tickers])
        weights = weights / weights.sum()

        dropped = set(tickers) - set(valid_tickers)
        if dropped:
            st.warning(
                f"Os seguintes tickers não possuem dados no período e foram ignorados: "
                f"{', '.join(sorted(dropped))}"
            )

        PortfolioView.show_prices(prices, frequency=frequency)

        model = PortfolioModel(prices, weights)
        metrics = {
            "Expected Return": model.expected_return(),
            "Volatility": model.volatility(),
            "Sharpe": model.sharpe_ratio(),
            "Max Drawdown": model.max_drawdown(),
            "VaR": model.var(),
            "CVaR": model.cvar()
        }

        frontier_results, opt_weights, opt_metrics = model.efficient_frontier()

        sims = model.simulate_monte_carlo(simulations)
        corr = model.correlation_matrix()

        PortfolioView.show_results(
            cumulative_series=model.cumulative_returns(),
            metrics=metrics,
            sims=sims,
            corr=corr,
            portfolio_returns=model.portfolio_returns(),
            frontier_results=frontier_results,
            opt_weights=opt_weights,
            tickers=valid_tickers,
            opt_metrics=opt_metrics,
        )
        