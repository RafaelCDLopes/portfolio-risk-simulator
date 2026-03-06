import streamlit as st
from src.controllers.portfolio_controller import PortfolioController

st.set_page_config(
    page_title="Portfolio Risk Simulator",
    page_icon="📈",
    layout="wide",
)

def _inject_global_styles():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

_inject_global_styles()

with st.sidebar:
    st.markdown("## 📈 Portfolio Lab")
    st.caption("Ferramentas quantitativas de risco")

    st.divider()

    if st.button("📊 Simulador de portfólio", use_container_width=True):
        st.session_state.page = "portfolio"

    if st.button("⚠️ Risk Dashboard", use_container_width=True):
        st.session_state.page = "risk"

    st.divider()

# Página padrão
if "page" not in st.session_state:
    st.session_state.page = "portfolio"

if st.session_state.page == "portfolio":
    PortfolioController().run()
elif st.session_state.page == "risk":
    st.title("⚠️ Risk Dashboard")
    st.info("Em breve: visão consolidada de risco do portfólio.")
