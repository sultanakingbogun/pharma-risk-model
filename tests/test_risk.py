"""Checks that the risk functions give the right answer on data where
the answer is known in advance."""
import numpy as np
import pandas as pd
import pytest
from scipy import stats

from pharmarisk import backtest, stress, var


def test_kupiec_accepts_right_rate_and_rejects_wrong_one():
    """10 breaches in 1,000 days at 99% is exactly right; 30 is far too many."""
    assert backtest.kupiec_test(10, 1000, 0.99) > 0.5
    assert backtest.kupiec_test(30, 1000, 0.99) < 0.01


def test_christoffersen_spots_clustering():
    """Ten breaches in a row should be flagged; ten spread evenly should not."""
    clustered = np.zeros(1000, dtype=bool)
    clustered[500:510] = True
    spread = np.zeros(1000, dtype=bool)
    spread[::100] = True
    assert backtest.christoffersen_test(clustered) < 0.01
    assert backtest.christoffersen_test(spread) > 0.05


def test_concentrated_weights_add_up_to_100_percent():
    weights = stress.concentrated_weights(["A", "B", "C", "D", "E"], "C", 0.4)
    assert weights.sum() == pytest.approx(1.0)
    assert weights["C"] == 0.4


def test_sector_shock_loses_the_shock_size():
    """Every stock falling 12% must cost the portfolio exactly 12%."""
    returns = pd.Series(np.random.default_rng(0).normal(0, 0.01, 250))
    loss, _ = stress.sector_shock(returns, shock=-0.12)
    assert loss == pytest.approx(0.12)


def test_historical_var_on_constant_losses():
    """If every day loses exactly 1%, VaR at any confidence level is 1%."""
    returns = pd.Series([-0.01] * 250)
    assert var.historical_var(returns, 0.99) == pytest.approx(0.01)
    assert var.historical_var(returns, 0.95) == pytest.approx(0.01)


def test_var_matches_bell_curve_theory():
    """On a huge sample of bell-curve returns, both methods should land on the
    textbook answer: 2.33 standard deviations below the average."""
    rng = np.random.default_rng(1)
    returns = pd.Series(rng.normal(0, 0.01, size=200_000))
    theory = -stats.norm.ppf(0.01) * 0.01
    assert var.parametric_var(returns, 0.99) == pytest.approx(theory, rel=0.01)
    assert var.historical_var(returns, 0.99) == pytest.approx(theory, rel=0.02)


def test_traffic_light_boundaries():
    """Basel zones: 0-4 green, 5-9 amber, 10+ red."""
    assert backtest.traffic_light(0) == "Green"
    assert backtest.traffic_light(4) == "Green"
    assert backtest.traffic_light(5) == "Amber"
    assert backtest.traffic_light(9) == "Amber"
    assert backtest.traffic_light(10) == "Red"
