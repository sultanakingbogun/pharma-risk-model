"""1-day Value-at-Risk: how much the portfolio could lose in a day.

Results are losses as a positive fraction of the portfolio,
so 0.025 means a loss of 2.5%.
"""
import numpy as np


def historical_var(port_returns, confidence):
    """The loss exceeded on only (1 - confidence) of past days.

    Assumes tomorrow looks like a random one of the days in the data,
    with no formula or distribution needed.
    """
    return -np.quantile(port_returns, 1 - confidence)


def historical_es(port_returns, confidence):
    """Average loss on the days that were worse than the VaR cut-off."""
    cutoff = np.quantile(port_returns, 1 - confidence)
    worst_days = port_returns[port_returns <= cutoff]
    return -worst_days.mean()

