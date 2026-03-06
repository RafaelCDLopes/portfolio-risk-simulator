import numpy as np
from src.models.portfolio_models import PortfolioModel
from src.services.data_loader import DataLoader
from src.services.simulation_service import MonteCarloService
from src.views.portfolio_view import PortfolioView

class PortfolioController:
    def run(self):
        tickers, start, end, simulations = PortfolioView.input_section()
        tickers = [t.strip() for t in tickers.split(",")]
        weights = PortfolioView.weight_section(tickers)
        run = PortfolioView.run_button()

        if not run:
            return

        if sum(weights) == 0:
            return

        weights = np.array(weights) / sum(weights)
        prices = DataLoader.load_prices(tickers, start, end)

        PortfolioView.show_prices(prices)

        model = PortfolioModel(prices, weights)
        metrics = {
            "Expected Return": model.expected_return(),
            "Volatility": model.volatility(),
            "Sharpe": model.sharpe_ratio(),
            "Max Drawdown": model.max_drawdown(),
            "VaR": model.var(),
            "CVaR": model.cvar()
        }

        sims = MonteCarloService.simulate(prices, weights, simulations)

        returns = PortfolioModel.returns(prices)
        corr = PortfolioModel.correlation_matrix(returns)

        PortfolioView.show_results(
            cumulative_series=model.cumulative_returns(),
            metrics=metrics,
            sims=sims,
            corr=corr,
            portfolio_returns=model.portfolio_returns(),
        )