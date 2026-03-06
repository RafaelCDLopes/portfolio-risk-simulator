import yfinance as yf
import pandas as pd

TICKERS = list(set([
    "AAPL",
    "MSFT",
    "SPY",
    "NVDA",
    "GOOGL",
    "AMZN",
    "PETR4.SA",
    "VALE3.SA",
    "GLD",
    "BTC-USD"
]))

DATA_PATH = "data"

def download_prices():
    data = {}
    for ticker in TICKERS:
        print(f"Downloading {ticker}...")
        df = yf.Ticker(ticker).history(period="10y", auto_adjust=True)
        if df.empty:
            print(f"⚠ No data for {ticker}")
            continue
        close = df["Close"].copy()
        close.index = pd.to_datetime(close.index)

        if close.index.tz is not None:
            close.index = close.index.tz_localize(None)

        close.index = close.index.normalize()
        data[ticker] = close

    prices = pd.DataFrame(data).sort_index()
    prices = prices.ffill()

    return prices

def create_datasets(prices):
    daily = prices.copy()
    weekly = (
        prices
        .resample("W-FRI")
        .last()
        .ffill()
    )
    monthly = (
        prices
        .resample("ME")
        .last()
        .ffill()
    )
    return daily, weekly, monthly


def save_datasets(daily, weekly, monthly):
    daily.to_parquet(f"{DATA_PATH}/prices_daily.parquet")
    weekly.to_parquet(f"{DATA_PATH}/prices_weekly.parquet")
    monthly.to_parquet(f"{DATA_PATH}/prices_monthly.parquet")

    print("Datasets saved:")
    print("  prices_daily.parquet")
    print("  prices_weekly.parquet")
    print("  prices_monthly.parquet")



prices = download_prices()
daily, weekly, monthly = create_datasets(prices)
save_datasets(daily, weekly, monthly)