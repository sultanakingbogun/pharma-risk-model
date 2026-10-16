"""All the assumptions behind the risk model, kept in one place so every
number in the report can be traced back to a deliberate choice."""

# Ten pharma and biotech stocks, all traded in the US in dollars. This avoids
# mixing currency risk into the results and keeps every stock on the same
# trading calendar. Ticker symbols are what yfinance downloads; the company
# names are for chart labels.
TICKERS = {
    "AZN": "AstraZeneca",
    "GSK": "GSK",
    "NVO": "Novo Nordisk",
    "PFE": "Pfizer",
    "LLY": "Eli Lilly",
    "MRK": "Merck & Co",
    "SNY": "Sanofi",
    "MRNA": "Moderna",
    "BNTX": "BioNTech",
    "SRPT": "Sarepta Therapeutics",
}

# Large companies with many drugs vs. smaller biotechs whose value depends
# on a few products, so a single trial result can move them sharply.
LARGE_PHARMA_TICKERS = ["AZN", "GSK", "NVO", "PFE", "LLY", "MRK", "SNY"]
SMALL_BIOTECH_TICKERS = ["MRNA", "BNTX", "SRPT"]

# $1m split equally: $100,000 in each stock, reset to equal weights daily.
PORTFOLIO_VALUE = 1_000_000

# About one trading year of history behind each VaR estimate. Enough data
# to contain 2-3 days in the worst 1% tail, recent enough to reflect current
# conditions, and the minimum bank regulators (Basel) require.
ESTIMATION_WINDOW = 250

# 99% = the loss exceeded on about 1 trading day in 100 (~2.5 days a year).
# 95% is included because its ~12 expected breaches a year give the backtest
# enough events to judge whether a model is accurate or just lucky.
CONFIDENCE_LEVELS = [0.95, 0.99]

# Expected Shortfall level used by the Basel (FRTB) capital rules.
ES_LEVEL = 0.975


# Starts early enough to replay the March 2020 COVID crash in the stress tests.
DATA_START = "2019-06-01"


# Monte Carlo: number of simulated days, and the random seed so the
# "random" draws come out identical on every run (results are repeatable).
MC_SIMULATIONS = 10_000
RANDOM_SEED = 42


# Student-t degrees of freedom for Monte Carlo: lower = fatter tails.
# 5 is a common choice for daily stock returns.
MC_T_DF = 5


# Sector-wide shock (e.g. US drug-pricing policy or tariffs). Large pharma fell
# about 15% over 20 days twice recently (Nov 2024, Apr 2025); -12% is a
# slightly milder one-off hit.
SECTOR_SHOCK = -0.12


# Single-stock "trial failure": one biotech drops 30% overnight. Tested with
# that stock making up 5% to 50% of the portfolio.
TRIAL_FAILURE_SHOCK = -0.30
CONCENTRATIONS = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50]


# March 2020 COVID crash, from the S&P 500's pre-crash high to its low.
COVID_PEAK = "2020-02-19"
COVID_TROUGH = "2020-03-23"
