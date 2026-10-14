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

