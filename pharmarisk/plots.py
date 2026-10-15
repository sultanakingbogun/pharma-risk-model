"""Charts for the report, saved as PNG files."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter

from . import config


# Three chart colours from a palette tested to stay distinguishable for
# colour-blind readers, plus greys for text, axes and grid lines.
BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"
INK, INK_2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#fcfcfb"

# House style applied to every chart: light background, no top/right border,
# faint grid lines, grey text, titles bold and left-aligned.
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK_2, "xtick.color": INK_2,
    "ytick.color": INK_2, "text.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.titleweight": "bold", "axes.titlesize": 12, "axes.titlelocation": "left",
})


def loss_distribution(port_returns, var99, path):
    """Histogram of daily losses, with each method's 99% VaR as a vertical line.

    `var99` is a dictionary of method name -> 99% VaR (as a decimal).
    """
    losses = -port_returns * 100
    right = max(losses.max(), max(var99.values()) * 100) + 0.5

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.hist(losses, bins=40, range=(-6, right), color=BLUE, alpha=0.35,
            label="Daily losses")

    styles = [(BLUE, "-"), (ORANGE, "--"), (AQUA, "-.")]
    for (name, value), (color, line) in zip(var99.items(), styles):
        ax.axvline(value * 100, color=color, linestyle=line, linewidth=2,
                   label=f"{name} 99% VaR: {value:.2%}")

    ax.set_xlim(-6, right)
    off_scale = losses[losses < -6]
    if len(off_scale) > 0:
        ax.annotate(f"{len(off_scale)} gain day off scale: +{-off_scale.min():.0f}%",
                    xy=(-6, 0), xytext=(4, 40), textcoords="offset points",
                    fontsize=8.5, color=INK_2,
                    arrowprops=dict(arrowstyle="->", color=MUTED))

    ax.set_title("Daily portfolio losses vs 99% VaR (last 250 days)")
    ax.set_xlabel("Daily loss (% of portfolio value; right = bigger loss)")
    ax.set_ylabel("Number of days")
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def backtest_chart(port_returns, forecast, method_name, path):
    """Daily returns over time against the 99% VaR line, with breaches marked."""
    returns = port_returns.loc[forecast.index] * 100
    var_line = -forecast * 100
    breaches = returns < var_line

    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.bar(returns.index, returns, width=1.0, color=MUTED, alpha=0.6,
           label="Daily return")
    ax.plot(var_line.index, var_line, color=BLUE, linewidth=1.6,
            label=f"{method_name} 99% VaR")
    ax.scatter(returns.index[breaches], returns[breaches], color=RED, s=22,
               zorder=3, edgecolor=SURFACE, linewidth=1,
               label=f"Breach ({breaches.sum()} days)")

    limit = -returns.min() + 1
    ax.set_ylim(-limit, limit)
    ax.set_title(f"Backtest: {method_name} 99% VaR vs. actual daily returns")
    ax.set_ylabel("Daily return")
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.legend(loc="upper left", frameon=False, fontsize=8.5, ncol=3)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def concentration_chart(trial, path):
    """Trial-failure loss vs. VaR as the weight in one biotech grows.

    `trial` is the table from analysis.trial_failure_table.
    """
    weights = [c * 100 for c in config.CONCENTRATIONS]
    fig, ax = plt.subplots(figsize=(7, 3.8))

    colours = [BLUE, ORANGE, AQUA]
    for colour, (stock, rows) in zip(colours, trial.groupby("Stock", sort=False)):
        ax.plot(weights, rows["Own VaR ($)"] / 1000, color=colour, linewidth=2,
                linestyle="--", marker="o", markersize=5,
                label=f"99% VaR, {stock}-heavy portfolio")

    loss = trial.drop_duplicates("Weight")["Loss ($)"] / 1000
    ax.plot(weights, loss, color=INK, linewidth=2.2, marker="o", markersize=5,
            label="Trial-failure loss (-30% on one stock)")

    ax.set_title("Concentration: trial-failure loss outgrows VaR")
    ax.set_xlabel("Weight in the stock hit by the trial failure")
    ax.set_ylabel("Loss")
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}k"))
    ax.legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
