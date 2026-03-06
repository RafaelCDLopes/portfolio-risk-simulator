import streamlit as st
from src.controllers.portfolio_controller import PortfolioController

st.set_page_config(
    page_title="Portfolio Risk Simulator",
    page_icon="📈",
    layout="wide"
)

# ---------- SIDEBAR ----------
with st.sidebar:

    st.markdown("## 📈 Portfolio Lab")
    st.caption("Quantitative Risk Tools")

    st.divider()

    if st.button("📊 Portfolio Simulator", use_container_width=True):
        st.session_state.page = "portfolio"

    if st.button("⚠️ Risk Dashboard", use_container_width=True):
        st.session_state.page = "risk"

    if st.button("🎲 Monte Carlo Lab", use_container_width=True):
        st.session_state.page = "montecarlo"

    st.divider()

# default page
if "page" not in st.session_state:
    st.session_state.page = "portfolio"

# ---------- ROUTER ----------
if st.session_state.page == "portfolio":
    PortfolioController().run()

elif st.session_state.page == "risk":
    st.title("Risk Dashboard (coming soon)")

elif st.session_state.page == "montecarlo":
    st.title("Monte Carlo Lab (coming soon)")