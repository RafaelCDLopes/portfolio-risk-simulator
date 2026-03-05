import streamlit as st
from datetime import date
import numpy as np
from src.data_loader import DataLoader
from src.statistics import calculate_log_returns, historical_mean, covariance_matrix
from src.portfolio import portfolio_return, cumulative_return
from src.risk_metrics import portfolio_volatility, portfolio_sharpe, max_drawdown, var_historical, cvar_historical
from src.simulation import monte_carlo_simulation
import pandas as pd

st.title("Portfolio Risk Simulator")

# Sidebar
st.sidebar.header("Input Parameters")
ticker_input = st.sidebar.text_input("Enter tickers (comma separated)", value="AAPL, MSFT, SPY")
start_date = st.sidebar.date_input("Start Date", date(2018, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2024, 1, 1))
weights_input = st.sidebar.text_input("Enter weights (comma separated, sum=1)", value="0.33,0.33,0.34")
num_simulations = st.sidebar.number_input("Monte Carlo Simulations", value=1000, step=100)

if st.sidebar.button("Run Simulation"):
   try:
      # Load prices
      loader = DataLoader(ticker_input, start_date, end_date)
      prices = loader.download_data()

      # Parse weights
      weights = np.array([float(w.strip()) for w in weights_input.split(",")])
      if not np.isclose(weights.sum(), 1.0):
         st.error("Weights must sum to 1.")
      elif len(weights) != prices.shape[1]:
         st.error("Number of weights must match number of tickers.")
      else:
         # Statistics
         returns = calculate_log_returns(prices)
         mean_returns = historical_mean(returns)
         cov_matrix = covariance_matrix(returns)

         # Portfolio
         port_returns = portfolio_return(returns, weights)
         port_cum_returns = cumulative_return(port_returns)

         # Risk metrics
         vol = portfolio_volatility(port_returns)
         sharpe = portfolio_sharpe(port_returns)
         mdd = max_drawdown(port_cum_returns)
         var = var_historical(port_returns)
         cvar = cvar_historical(port_returns)

         # Monte Carlo
         num_days = 252
         mc = monte_carlo_simulation(weights, mean_returns.values, cov_matrix.values, num_days=num_days, num_simulations=num_simulations)
         last_date = prices.index[-1]
         mc_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=num_days, freq='B')

         mc_df = pd.DataFrame(mc.T, index=mc_index)

         # Display
         st.subheader("Price Data")
         st.dataframe(prices)

         st.subheader("Portfolio Cumulative Returns")
         st.line_chart(port_cum_returns)

         st.subheader("Portfolio Risk Metrics")
         st.table({
            "Volatility": [vol],
            "Sharpe Ratio": [sharpe],
            "Max Drawdown": [mdd],
            "VaR (5%)": [var],
            "CVaR (5%)": [cvar]
         })

         st.subheader("Monte Carlo Simulation")
         st.line_chart(mc_df)

   except Exception as e:
      st.error(f"Error: {e}")