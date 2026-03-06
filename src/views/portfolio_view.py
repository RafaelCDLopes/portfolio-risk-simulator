import numpy as np
import seaborn as sns
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt


class PortfolioView:
    @staticmethod
    def input_section():
        st.title("📊 Simulador de Risco de Portfólio")
        st.caption(
            "Explore o comportamento do seu portfólio ao longo do tempo, "
            "com simulações de Monte Carlo e métricas de risco clássicas."
        )

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                tickers = st.text_input(
                    "Tickers (separados por vírgula)",
                    "PETR4.SA,VALE3.SA,ITUB4.SA",
                    help="Use os códigos do Yahoo Finance, separados por vírgula."
                )

            with col2:
                simulations = st.number_input(
                    "Número de simulações (Monte Carlo)",
                    min_value=100,
                    max_value=10000,
                    value=1000,
                    step=100,
                    help="Quantidade de trajetórias simuladas do portfólio."
                )

        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input(
                "Data inicial",
                value=date(2018, 1, 1),
                help="Data inicial da série histórica utilizada."
            )

        with col2:
            end = st.date_input(
                "Data final",
                value=date(2024, 1, 1),
                help="Data final da série histórica utilizada."
            )

        return tickers, start, end, simulations

    @staticmethod
    def weight_section(tickers):
        st.subheader("⚖️ Pesos do Portfólio")
        st.caption("Defina a alocação alvo de cada ativo. A soma será normalizada automaticamente.")

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
        return st.button("🚀 Rodar simulação", use_container_width=True)

    @staticmethod
    def show_prices(prices):
        with st.expander("📈 Dados de preços (ajustados)"):
            st.dataframe(prices)

    @staticmethod
    def show_cumulative_returns(series):
        st.subheader("📊 Retorno acumulado do portfólio")
        st.line_chart(series)

    @staticmethod
    def show_metrics(metrics):
        st.subheader("📉 Métricas de risco")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Retorno esperado", f"{metrics['Expected Return']:.2%}")
        col2.metric("Volatilidade", f"{metrics['Volatility']:.2%}")
        col3.metric("Índice de Sharpe", f"{metrics['Sharpe']:.2f}")
        col4.metric("VaR (5%)", f"{metrics['VaR']:.2%}")
        col5.metric("CVaR (5%)", f"{metrics['CVaR']:.2%}")

        st.metric("Máx. drawdown", f"{metrics['Max Drawdown']:.2%}")

    @staticmethod
    def show_simulation(df):
        st.subheader("🎲 Simulação Monte Carlo")
        st.line_chart(df)

    @staticmethod
    def show_correlation(corr):
        st.subheader("🔥 Correlação entre ativos")

        fig, ax = plt.subplots()
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            ax=ax
        )

        st.pyplot(fig)

    @staticmethod
    def show_var_distribution(portfolio_returns):
        st.subheader("📉 Distribuição de retornos e VaR")

        fig, ax = plt.subplots()
        ax.hist(portfolio_returns, bins=50)
        var = np.percentile(portfolio_returns, 5)
        ax.axvline(var)

        st.pyplot(fig)

    @staticmethod
    def show_results(cumulative_series, metrics, sims, corr, portfolio_returns):
        st.markdown("## 📊 Resultados da simulação")

        tab_overview, tab_risk, tab_sim = st.tabs(
            ["Resumo", "Risco & correlação", "Cenários Monte Carlo"]
        )

        with tab_overview:
            PortfolioView.show_cumulative_returns(cumulative_series)
            PortfolioView.show_metrics(metrics)

        with tab_risk:
            PortfolioView.show_correlation(corr)
            PortfolioView.show_var_distribution(portfolio_returns)

        with tab_sim:
            PortfolioView.show_simulation(sims)

    @staticmethod
    def show_efficient_frontier(results):
        st.subheader("📊 Efficient Frontier")

        fig, ax = plt.subplots()
        ax.scatter(
            results[:,0],
            results[:,1],
            c=results[:,2],
            cmap="viridis"
        )
        ax.set_xlabel("Volatility")
        ax.set_ylabel("Return")

        st.pyplot(fig)