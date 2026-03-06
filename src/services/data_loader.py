import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


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
    def load_prices(tickers, start=None, end=None):
        start, end = DataLoader._validate_dates(start, end)
        data = pd.DataFrame()

        for ticker in tickers:
            df = yf.Ticker(ticker).history(
                start=start,
                end=end,
                auto_adjust=True
            )

            if df.empty:
                raise ValueError(f"No data returned for {ticker}")
            if "Close" not in df.columns:
                raise ValueError(f"'Close' column not found for {ticker}")
            data[ticker] = df["Close"]
        data = data.dropna()

        if data.shape[0] < 2:
            raise ValueError("Not enough data after cleaning.")

        return data