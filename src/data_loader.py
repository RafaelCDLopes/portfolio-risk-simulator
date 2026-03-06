import yfinance as yf
import pandas as pd

class DataLoader:
    def __init__(self, ticker_string: str, start_date, end_date):
        self.ticker_string = ticker_string
        self.start_date = start_date
        self.end_date = end_date
        self.tickers = self._parse_tickers()

    def _parse_tickers(self) -> list:
        if not self.ticker_string:
            raise ValueError("Ticker input cannot be empty.")

        tickers = [
            ticker.strip().upper()
            for ticker in self.ticker_string.split(",")
            if ticker.strip() != ""
        ]

        if len(tickers) == 0:
            raise ValueError("No valid tickers provided.")

        return tickers

    def download_data(self) -> pd.DataFrame:
        data = yf.download(
            tickers=self.tickers,
            start=self.start_date,
            end=self.end_date,
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if data.empty:
            raise ValueError("No data returned. Check tickers or date range.")

        # Verifica se é multi-ticker
        if isinstance(data.columns, pd.MultiIndex):
            if "Adj Close" in data.columns.levels[0]:
                data = data["Adj Close"]
            elif "Close" in data.columns.levels[0]:
                data = data["Close"]
            else:
                raise ValueError("No Close or Adjusted Close available for selected tickers.")
        else:
            # Single ticker
            if "Adj Close" in data.columns:
                data = data[["Adj Close"]]
            elif "Close" in data.columns:
                data = data[["Close"]]
            else:
                raise ValueError("No Close or Adjusted Close available.")

            data.columns = self.tickers

        # Limpa dados faltantes
        data = data.dropna()

        if data.shape[0] < 2:
            raise ValueError("Not enough data points after cleaning.")

        return data