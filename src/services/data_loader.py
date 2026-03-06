import pandas as pd
from datetime import datetime, timedelta
from src.utils.finance_utils import normalize_ticker

class DataLoader:
    DEFAULT_YEARS = 2

    DATASETS = {
        "D": "data/prices_daily.parquet",
        "W": "data/prices_weekly.parquet",
        "M": "data/prices_monthly.parquet",
    }

    @staticmethod
    def _validate_dates(start, end):
        today = datetime.today()
        if end is None:
            end = today
        if start is None:
            start = end - timedelta(days=365 * DataLoader.DEFAULT_YEARS)

        start = pd.to_datetime(start).tz_localize(None)
        end = pd.to_datetime(end).tz_localize(None)

        if start >= end:
            raise ValueError("Start date must be earlier than end date.")
        
        return start, end

    @staticmethod
    def _load_dataset(frequency):
        if frequency not in DataLoader.DATASETS:
            raise ValueError("Frequency must be 'D', 'W', or 'M'")

        path = DataLoader.DATASETS[frequency]
        data = pd.read_parquet(path)
        data.index = pd.to_datetime(data.index)

        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)

        data.index = data.index.normalize()

        return data

    @staticmethod
    def load_prices(tickers, start=None, end=None, frequency="D"):
        start, end = DataLoader._validate_dates(start, end)
        data = DataLoader._load_dataset(frequency)
        tickers = [normalize_ticker(t) for t in tickers]
        available = data.columns
        invalid = [t for t in tickers if t not in available]

        if invalid:
            raise ValueError(f"Tickers not available in dataset: {invalid}")

        data = data[tickers]
        data = data.loc[start:end]

        if data.empty:
            raise ValueError("No data available in selected period.")
        data = data.dropna()

        if data.shape[0] < 2:
            raise ValueError("Not enough data points after filtering.")

        return data