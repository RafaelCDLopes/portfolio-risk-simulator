import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from src.utils.finance_utils import normalize_ticker


class DataLoader:
    DEFAULT_YEARS = 2

    @staticmethod
    def _validate_dates(start, end):
        """
        Ensures valid date range. If missing, apply default window.
        """
        today = datetime.today()

        if end is None:
            end = today
        if start is None:
            start = end - timedelta(days=365 * DataLoader.DEFAULT_YEARS)
        if start >= end:
            raise ValueError("Start date must be earlier than end date.")

        return start, end

    @staticmethod
    def load_prices(tickers, start=None, end=None, frequency="D"):
        """
        Carrega preços e padroniza o período para comparação justa entre ativos.

        frequency: "D" = diário, "W" = semanal (sexta), "M" = mensal (fim do mês)
        """
        start, end = DataLoader._validate_dates(start, end)
        data = pd.DataFrame()
        for ticker in tickers:
            ticker = normalize_ticker(ticker)
            df = yf.Ticker(ticker).history(
                start=start,
                end=end,
                auto_adjust=True
            )
            if df.empty:
                raise ValueError(f"No data returned for {ticker}")
            if "Close" not in df.columns:
                raise ValueError(f"'Close' column not found for {ticker}")
            close = df["Close"].copy()
            close.index = pd.to_datetime(close.index)
            if close.index.tz is not None:
                close.index = close.index.tz_localize(None)
            close.index = close.index.normalize()
            data[ticker] = close
        if data.empty:
            raise ValueError("No data downloaded for selected tickers and period.")
        # 1) achar primeira e última data válida de cada ativo;
        #    ignora tickers sem dados (ex: alinhamento por timezone diferente)
        first_dates = []
        last_dates = []
        valid_cols = []
        for col in data.columns:
            series = data[col].dropna()
            if series.empty:
                continue
            first_dates.append(series.index[0])
            last_dates.append(series.index[-1])
            valid_cols.append(col)

        if not valid_cols:
            raise ValueError(
                "Nenhum dos tickers possui dados no período selecionado. "
                "Ajuste as datas ou revise os códigos informados."
            )

        data = data[valid_cols]

        # 2) intervalo comum
        common_start = max(first_dates)
        common_end = min(last_dates)
        if common_start >= common_end:
            raise ValueError(
                "Não existe intervalo de datas em comum entre todos os ativos "
                "dentro do período selecionado."
            )
        # 3) restringe ao intervalo comum e remove eventuais NaNs restantes
        data = data.loc[common_start:common_end].dropna()

        # 4) resample para frequência padronizada (permite comparação justa)
        if frequency == "W":
            data = data.resample("W-FRI").last().dropna()  # sexta-feira
        elif frequency == "M":
            data = data.resample("ME").last().dropna()   # fim do mês

        if data.shape[0] < 2:
            raise ValueError(
                "Não há dados suficientes mesmo após ajustar o intervalo comum."
            )
        return data