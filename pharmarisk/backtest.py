"""Backtesting: would the VaR models have been right in the past?"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import xlogy

from . import config
from .var import historical_var


def rolling_var(port_returns, confidence, method=historical_var,     
                window=config.ESTIMATION_WINDOW):                    
    """VaR forecast for each day, using only the `window` days before it.

    `method` can be any of the VaR functions in var.py.               
    No look-ahead: the forecast for day i uses returns up to day i-1 only.
    """
    forecasts = {}
    for i in range(window, len(port_returns)):
        past = port_returns.iloc[i - window : i]
        forecasts[port_returns.index[i]] = method(past, confidence)
    return pd.Series(forecasts)


def kupiec_test(breaches, days, confidence):
    """Kupiec (1995) test: is the breach rate consistent with the confidence level?

    Returns a p-value. Below 0.05 means the model breached too often (or too
    rarely) to be explained by bad luck, so it fails.
    """
    expected_rate = 1 - confidence
    actual_rate = breaches / days
    log_if_model_right = xlogy(days - breaches, 1 - expected_rate) + xlogy(breaches, expected_rate)
    log_if_actual_rate = xlogy(days - breaches, 1 - actual_rate) + xlogy(breaches, actual_rate)
    test_stat = -2 * (log_if_model_right - log_if_actual_rate)
    return 1 - stats.chi2.cdf(test_stat, df=1)


def traffic_light(breaches):
    """Basel zone for a 99% VaR model, from breaches in the last 250 days.

    Green 0-4 (accepted), amber 5-9 (capital penalty), red 10+ (model rejected).
    """
    if breaches <= 4:
        return "Green"
    if breaches <= 9:
        return "Amber"
    return "Red"


def christoffersen_test(hits):
    """Christoffersen (1998) test: do breaches cluster in time?

    `hits` is True/False for each day (True = breach). A good model's breaches
    should be independent: a breach today shouldn't make one tomorrow more
    likely. Returns a p-value; below 0.05 means breaches cluster.
    """
    h = np.asarray(hits, dtype=int)
    yesterday, today = h[:-1], h[1:]

    n00 = np.sum((yesterday == 0) & (today == 0))
    n01 = np.sum((yesterday == 0) & (today == 1))
    n10 = np.sum((yesterday == 1) & (today == 0))
    n11 = np.sum((yesterday == 1) & (today == 1))

    rate_after_calm = n01 / max(n00 + n01, 1)
    rate_after_breach = n11 / max(n10 + n11, 1)
    overall_rate = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)

    log_same = xlogy(n00 + n10, 1 - overall_rate) + xlogy(n01 + n11, overall_rate)
    log_different = (xlogy(n00, 1 - rate_after_calm) + xlogy(n01, rate_after_calm)
                     + xlogy(n10, 1 - rate_after_breach) + xlogy(n11, rate_after_breach))
    test_stat = -2 * (log_same - log_different)
    return 1 - stats.chi2.cdf(test_stat, df=1)
