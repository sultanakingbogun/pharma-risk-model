"""Stress tests: losses in specific bad scenarios, compared with VaR."""
import pandas as pd

from . import config
from .data import portfolio_returns
from .var import historical_var


def sector_shock(port_returns, shock=config.SECTOR_SHOCK,
                 window=config.ESTIMATION_WINDOW, confidence=0.99):
    """Every stock falls by `shock` at once.

    Returns the portfolio loss and how many times 99% VaR that is.
    Diversification doesn't help when the whole sector falls together.
    """
    loss = -shock
    var_99 = historical_var(port_returns.tail(window), confidence)
    return loss, loss / var_99


def concentrated_weights(tickers, target, concentration):
    """Put `concentration` in the target stock and split the rest equally."""
    others =     others = (1 - concentration) / (len(tickers) - 1)

    weights = pd.Series(others, index=tickers)
    weights[target] = concentration
    return weights


def trial_failure(returns, target, concentration, shock=config.TRIAL_FAILURE_SHOCK,
                  window=config.ESTIMATION_WINDOW, confidence=0.99):
    """One stock (`target`) falls by `shock`, with `concentration` of the portfolio in it.

    Returns the scenario loss, and the 99% VaR of that concentrated portfolio.
    """
    weights = concentrated_weights(returns.columns, target, concentration)
    loss = -concentration * shock
    port = portfolio_returns(returns, weights).tail(window)
    return loss, historical_var(port, confidence)
