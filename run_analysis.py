"""Run the full analysis and save every results table and chart to output/.

    python run_analysis.py              # uses saved prices if present
    python run_analysis.py --refresh    # downloads fresh prices first
"""
import argparse
from pathlib import Path

from pharmarisk import analysis, backtest, config, data, plots

OUT = Path("output")


def main():
    parser = argparse.ArgumentParser(description="Pharma portfolio risk analysis")
    parser.add_argument("--refresh", action="store_true", help="re-download prices")
    args = parser.parse_args()

    prices = data.download_prices(refresh=args.refresh)
    returns = data.to_returns(prices)
    port = data.portfolio_returns(returns)

    tables = {
        "var": analysis.var_table(port),
        "backtest": analysis.backtest_table(port),
        "stress": analysis.stress_table(prices, port),
        "trial_failure": analysis.trial_failure_table(returns, port),
    }

    OUT.mkdir(exist_ok=True)
    for name, table in tables.items():
        table.to_csv(OUT / f"{name}.csv", index=False)
        print(f"\n{name}:")
        print(table.to_string(index=False))
    print(f"\nTables saved to {OUT}/")

    recent = port.tail(config.ESTIMATION_WINDOW)
    var99 = {name: method(recent, 0.99) for name, method in analysis.METHODS.items()}
    plots.loss_distribution(recent, var99, OUT / "loss_distribution.png")

    forecast = backtest.rolling_var(port, 0.99)
    plots.backtest_chart(port, forecast, "Historical", OUT / "backtest_historical_99.png")

    plots.concentration_chart(tables["trial_failure"], OUT / "concentration_stress.png")
    print(f"Charts saved to {OUT}/")


if __name__ == "__main__":
    main()
