
"""Downloading prices and turning them into the returns the risk model uses."""
from pathlib import Path

import pandas as pd

from . import config

CACHE = Path("data/prices.csv")


def download_prices(refresh=False):
    """Daily closing prices for every stock in config.TICKERS.

    Saved to data/prices.csv after the first download, so later runs read
    the file instead of downloading again. Pass refresh=True to re-download.
    """
    tickers = list(config.TICKERS)

    if CACHE.exists() and not refresh:
        return pd.read_csv(CACHE, index_col=0, parse_dates=True)

    import yfinance as yf

    prices = yf.download(tickers, start=config.DATA_START, auto_adjust=True, progress=False)["Close"]
    CACHE.parent.mkdir(exist_ok=True)
    prices.to_csv(CACHE)
    return prices


def to_returns(prices):
    """Simple daily returns, one column per stock.

    The first day has no previous price, so it is dropped.
    """
    return prices.pct_change().dropna()


def portfolio_returns(returns, weights=None):
    """Daily return of the whole portfolio.

    Each day's return is the weighted average of the stocks' returns.
    With no weights given, every stock gets an equal share.
    """
    if weights is None:
        weights = 1 / len(returns.columns)

    return (returns * weights).sum(axis=1)
