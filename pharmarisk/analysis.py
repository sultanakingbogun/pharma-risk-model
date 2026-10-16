"""Runs every part of the analysis and collects the results as tables."""
import pandas as pd

from . import backtest, config, data, stress, var

METHODS = {
    "Historical": var.historical_var,
    "Parametric (normal)": var.parametric_var,
    "Monte Carlo (Student-t)": var.monte_carlo_var,
}


def var_table(port_returns):
    """Current 1-day VaR for every method and level, plus Expected Shortfall, in dollars."""
    recent = port_returns.tail(config.ESTIMATION_WINDOW)
    rows = []
    for level in config.CONFIDENCE_LEVELS:
        for name, method in METHODS.items():
            rows.append({
                "Measure": "VaR",
                "Confidence": f"{level:.0%}",
                "Method": name,
                "Loss ($)": round(method(recent, level) * config.PORTFOLIO_VALUE),
            })
    rows.append({
        "Measure": "Expected Shortfall",
        "Confidence": f"{config.ES_LEVEL:.1%}",
        "Method": "Historical",
        "Loss ($)": round(var.historical_es(recent, config.ES_LEVEL) * config.PORTFOLIO_VALUE),
    })
    return pd.DataFrame(rows)



def backtest_table(port_returns):
    """Backtest results for every method and confidence level."""
    rows = []
    for level in config.CONFIDENCE_LEVELS:
        for name, method in METHODS.items():
            forecast = backtest.rolling_var(port_returns, level, method=method)
            hits = -port_returns.loc[forecast.index] > forecast
            breaches = hits.sum()
            expected = len(forecast) * (1 - level)
            p = backtest.kupiec_test(breaches, len(forecast), level)
            verdict = "PASS" if p > 0.05 else "FAIL"
            p_cluster = backtest.christoffersen_test(hits)
            last_250 = hits.tail(250).sum()

            rows.append({
                "Confidence": f"{level:.0%}",
                "Method": name,
                "Days": len(forecast),
                "Expected breaches": round(expected, 1),
                "Actual breaches": breaches,
                "Kupiec p": round(p, 3),
                "Verdict": verdict,
                "Cluster p":round(p_cluster, 3),
                "Last 250d breaches": last_250,
                "Traffic light": backtest.traffic_light(last_250) if level == 0.99 else "n/a"
            })
    return pd.DataFrame(rows)


def stress_table(prices, port_returns):
    """Loss in each stress scenario, in dollars and as a multiple of 99% VaR."""
    current_var = var.historical_var(port_returns.tail(config.ESTIMATION_WINDOW), 0.99)
    sector_loss, _ = stress.sector_shock(port_returns)
    day, day_loss, covid_loss, _ = stress.covid_replay(prices)

    scenarios = {
        "Sector shock (-12% on every stock)": sector_loss,
        f"COVID worst day ({day:%d %b %Y})": day_loss,
        "COVID peak to trough (19 Feb - 23 Mar 2020)": covid_loss,
    }
    rows = []
    for name, loss in scenarios.items():
        rows.append({
            "Scenario": name,
            "Loss ($)": round(loss * config.PORTFOLIO_VALUE),
            "x 99% VaR": round(loss / current_var, 1),
        })
    return pd.DataFrame(rows)


def trial_failure_table(returns, port_returns):
    """Trial-failure loss for each small biotech at each concentration."""
    current_var = var.historical_var(port_returns.tail(config.ESTIMATION_WINDOW), 0.99)
    rows = []
    for ticker in config.SMALL_BIOTECH_TICKERS:
        for c in config.CONCENTRATIONS:
            loss, own_var = stress.trial_failure(returns, ticker, c)
            rows.append({
                "Stock": ticker,
                "Weight": f"{c:.0%}",
                "Loss ($)": round(loss * config.PORTFOLIO_VALUE),
                "x current VaR": round(loss / current_var, 1),
                "Own VaR ($)": round(own_var * config.PORTFOLIO_VALUE),
            })
    return pd.DataFrame(rows)
