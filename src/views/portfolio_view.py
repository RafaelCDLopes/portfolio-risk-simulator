import numpy as np
import seaborn as sns
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

AVAILABLE_TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "SPY",
    "GLD",
    "BTC-USD",
    "PETR4.SA",
    "VALE3.SA"
]

DEFAULT_TICKERS = ["SPY", "GLD", "BTC-USD"]

class PortfolioView:
    @staticmethod
    def input_section():
        st.title("📊 Simulador de Risco de Portfólio")
        st.caption(
            "Explore o comportamento do seu portfólio ao longo do tempo, "
            "com simulações de Monte Carlo e métricas de risco clássicas."
        )

        with st.container():
            col1, col2, col3 = st.columns(3)

            with col1:
                tickers = st.multiselect(
                    "Select assets for portfolio",
                    options=AVAILABLE_TICKERS,
                    default=DEFAULT_TICKERS,
                    help="Choose assets available in the dataset."
                )

            with col2:
                frequency = st.selectbox(
                    "Frequência dos dados",
                    options=["W", "M"],
                    format_func=lambda x: { "W": "Semanal", "M": "Mensal"}[x],
                    index=0,
                    help="Padroniza o período para comparação justa entre ativos (ex: BTC 24/7 vs ações em dias úteis)."
                )

            with col3:
                simulations = st.number_input(
                    "Número de simulações (Monte Carlo)",
                    min_value=100,
                    max_value=1000,
                    value=1000,
                    step=100,
                    help="Quantidade de trajetórias simuladas do portfólio."
                )

        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input(
                "Data inicial",
                value=date(2021, 1, 3),
                help="Data inicial da série histórica utilizada."
            )

        with col2:
            end = st.date_input(
                "Data final",
                value=date(2025, 12, 28),
                help="Data final da série histórica utilizada."
            )

        return tickers, start, end, simulations, frequency

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
    def show_prices(prices, frequency="W"):
        freq_label = {"W": "semanal", "M": "mensal"}.get(frequency, "semanal")
        with st.expander("📈 Dados de preços (ajustados)"):
            st.caption(f"Período padronizado para comparação (frequência: {freq_label})")
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

        with st.expander("O que significam essas métricas?"):
            st.markdown(
                """
- **Retorno esperado**: média histórica dos retornos do portfólio no período selecionado.
- **Volatilidade**: mede o quão “espalhados” são os retornos em torno da média (quanto maior, maior a variabilidade/risco).
- **Índice de Sharpe**: relação risco-retorno. Em geral, quanto maior, melhor (aqui usamos taxa livre de risco igual a 0).
- **VaR (5%)**: retorno no pior cenário típico de 5% dos casos — uma estimativa de “piora esperada” com 95% de confiança.
- **CVaR (5%)**: média dos retornos piores do que o VaR — captura a severidade dos eventos extremos (cauda da distribuição).
- **Máx. drawdown**: maior queda acumulada do pico até o vale ao longo do período analisado.

Observação: as métricas são calculadas sobre os retornos da frequência selecionada (diário/semanal/mensal) e do intervalo em que todos os ativos têm dados.
                """
            )

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
    def show_results(
        cumulative_series,
        metrics,
        sims,
        corr,
        portfolio_returns,
        frontier_results,
        opt_weights,
        tickers,
        opt_metrics,
    ):
        st.markdown("## 📊 Resultados da simulação")

        tab_overview, tab_risk, tab_sim, tab_frontier = st.tabs(
            ["Resumo", "Risco & correlação", "Cenários Monte Carlo", "Fronteira eficiente"]
        )

        with tab_overview:
            PortfolioView.show_cumulative_returns(cumulative_series)
            PortfolioView.show_metrics(metrics)

        with tab_risk:
            PortfolioView.show_correlation(corr)
            PortfolioView.show_var_distribution(portfolio_returns)

        with tab_sim:
            PortfolioView.show_simulation(sims)

        with tab_frontier:
            PortfolioView.show_efficient_frontier(frontier_results)

            st.markdown("### Portfólio de maior Sharpe")
            col1, col2, col3 = st.columns(3)
            col1.metric("Retorno esperado", f"{opt_metrics['Expected Return']:.2%}")
            col2.metric("Volatilidade", f"{opt_metrics['Volatility']:.2%}")
            col3.metric("Índice de Sharpe", f"{opt_metrics['Sharpe']:.2f}")

            st.markdown("#### Pesos ótimos")
            df_weights = pd.DataFrame(
                {"Ticker": tickers, "Peso": opt_weights}
            )
            df_weights["Peso"] = df_weights["Peso"].round(4)
            st.dataframe(df_weights, hide_index=True)

    @staticmethod
    def show_efficient_frontier(results):
        st.subheader("📊 Fronteira eficiente")

        fig, ax = plt.subplots()
        ax.scatter(
            results[:, 0],
            results[:, 1],
            c=results[:, 2],
            cmap="viridis"
        )
        ax.set_xlabel("Volatilidade")
        ax.set_ylabel("Retorno esperado")

        st.pyplot(fig)