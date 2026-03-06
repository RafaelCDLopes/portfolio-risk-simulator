import numpy as np
import streamlit as st
from datetime import date

class PortfolioView:
    @staticmethod
    def input_section():
        st.title("📊 Portfolio Risk Simulator")
        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                tickers = st.text_input(
                    "Tickers",
                    "PETR4.SA,VALE3.SA,ITUB4.SA,BBDC4.SA"
                )

            with col2:
                simulations = st.number_input(
                    "Monte Carlo Simulations",
                    min_value=100,
                    max_value=10000,
                    value=1000,
                    step=100
                )

        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input("Start Date", value=date(2018, 1, 1))

        with col2:
            end = st.date_input("End Date", value=date(2024, 1, 1))

        return tickers, start, end, simulations

    @staticmethod
    def weight_section(tickers):
        st.subheader("⚖️ Portfolio Weights")
        cols = st.columns(len(tickers))
        weights = []

        for i, ticker in enumerate(tickers):
            with cols[i]:
                w = st.number_input(
                    ticker,
                    min_value=0.0,
                    max_value=1.0,
                    value=round(1 / len(tickers), 2),
                    step=0.05
                )

                weights.append(w)

        return np.array(weights)

    @staticmethod
    def run_button():
        st.markdown("")
        return st.button("🚀 Run Simulation", use_container_width=True)

    @staticmethod
    def show_prices(prices):
        with st.expander("📈 Price Data"):
            st.dataframe(prices)

    @staticmethod
    def show_cumulative_returns(series):
        st.subheader("📊 Portfolio Cumulative Return")
        st.line_chart(series)

    @staticmethod
    def show_metrics(metrics):
        st.subheader("📉 Risk Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Expected Return", f"{metrics['Expected Return']:.2%}")
        col2.metric("Volatility", f"{metrics['Volatility']:.2%}")
        col3.metric("Sharpe", f"{metrics['Sharpe']:.2f}")
        col4.metric("VaR", f"{metrics['VaR']:.2%}")
        col5.metric("CVaR", f"{metrics['CVaR']:.2%}")

        st.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")

    @staticmethod
    def show_simulation(df):
        st.subheader("🎲 Monte Carlo Simulation")
        st.line_chart(df)