# app.py
import yfinance as yf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cotação B3", layout="centered")

st.title("📈 Cotação de Ações da B3")
ticker_input = st.text_input("Digite o ticker (ex: PETR4.SA)", value="PETR4.SA").upper()

try:
    data = yf.Ticker(ticker_input)
    hist = data.history(period="6mo")

    if hist.empty:
        st.warning("Ticker inválido ou sem dados.")
    else:
        last_price = hist["Close"].iloc[-1]

        # Variações
        def calc_var(days):
            idx = -min(days, len(hist))
            pct = ((last_price - hist["Close"].iloc[idx]) / hist["Close"].iloc[idx]) * 100
            return f"{pct:+.2f}%"

        st.metric("Último Preço", f"R$ {last_price:.2f}")
        st.markdown("### Variações")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("1D", calc_var(1))
        col2.metric("5D", calc_var(5))
        col3.metric("30D", calc_var(30))
        col4.metric("YTD", calc_var(len(hist)))

        st.markdown("### Gráfico de Preços (6 meses)")
        st.line_chart(hist["Close"])

except Exception as e:
    st.error(f"Erro ao buscar dados: {str(e)}")