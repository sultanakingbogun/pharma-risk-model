"""1-day Value-at-Risk: how much the portfolio could lose in a day.

Results are losses as a positive fraction of the portfolio,
so 0.025 means a loss of 2.5%.
"""
import numpy as np
from scipy import stats



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


def parametric_var(port_returns, confidence):
    """VaR assuming returns follow a normal distribution (bell curve).

    Only uses the average and the std of the returns, so a single extreme
    day affects the result through the std, even if it was a gain.
    """
    mean = port_returns.mean()
    std = port_returns.std()
    z = stats.norm.ppf(1 - confidence)
    return -(mean + z * std)


