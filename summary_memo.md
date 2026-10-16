# Pharma portfolio risk: summary

**To:** Head of Risk   **From:** Sultan Akingbogun   **Date:** 16 October 2026

## Bottom line

On most days the portfolio's losses stay below **$33,500**, the 99% one-day
VaR. We expect that line to be crossed on about 1 day(s) in 100, roughly
2-3 times a year. The historical model behind this number passed its
backtest: over the past six years it was crossed 18 times, close to
the 15 times we would expect.

The biggest risk is not a normal bad day but an event that hits every pharma
stock at once, such as a US drug-pricing or tariff announcement (large pharma fell about 15% in a month twice recently: after RFK Jr. was named health secretary in November 2024, and during the tariff threats of April 2025) A 12% fall across the
sector would cost **$120,000**, about 3.6× VaR. Holding ten different
stocks does not protect us from this, …because they would all fall together, so there are no gains elsewhere to offset the losses.


## How much could we lose in a day?

| Method | 95% VaR | 99% VaR |
|---|---|---|
| **Historical (recommended)** | $22,287 | $33,491 |
| Parametric (normal) | $32,955 | $47,292 |
| Monte Carlo (Student-t) | $31,668 | $52,357 |

- **What VaR means:** on 99 trading days out of 100, we expect to lose
  less than about $33,500. On the other 1, the loss will be larger,
  and VaR does not tell us by how much.
- **Expected Shortfall (97.5%): $32,885.** This is the average loss on the
  worst 2.5% of days, so it tells us how bad a bad day typically is.
  It is measured at 97.5%, the level regulators use, so it averages a slightly wider set of bad days and comes out close to 99% VaR rather than above it.
- **Why we recommend Historical:** it is based on what has actually happened over the past year (real daily returns),
  not on an assumed bell curve. The other two give figures about 40-56%
  higher, because one exceptional gain day (Moderna's vaccine trial results in August 2026, +24% for the portfolio) inflated their measure of volatility, so they count a windfall as risk..
- All figures use the last 250 trading days and a $1m portfolio with
  $100,000 in each stock.


## Can we trust the models?

We tested each model by going back day by day over the past six years:
each day we calculated VaR using only the previous year's data, then checked
whether the actual loss was bigger. A good 99% model should be crossed on
about ______ in 100 days.

- **Historical and Monte Carlo passed** at both 95% and 99%. Historical was
  crossed 18 times against 15.1 expected.
- **Parametric failed at 99%:** crossed 24 times against about 15.1
  expected, too many to be bad luck. It assumes returns follow a bell curve,
  but real markets have fat tails, so its 99% line is set
  too low, so real bad days go past it more often than it predicts. At 95% it passed, because the 95% line covers moderately bad days, where a bell curve is a reasonable fit. The difference only shows in the extreme tail..
- **All three models lean the same way:** every one was crossed more often
  than expected, at both levels. Even the models that passed tend to
  understate risk slightly.


## What could go badly wrong?

VaR only knows the last year, so we also tested three specific scenarios.

| Scenario | Loss | × 99% VaR |
|---|---|---|
| Sector shock: every stock falls 12% | $______ | ______× |
| COVID replay: worst single day (______ March 2020) | $______ | ______× |
| COVID replay: peak to trough (19 Feb – 23 Mar 2020) | $______ | ______× |
| Trial failure: one biotech falls 30%, at a 10% holding | $______ | ______× |
| Trial failure: same, at a 30% holding | $______ | ______× |

- **The sector shock is the largest risk.** ______________________
  [Why can't diversification help? You already wrote this in the bottom line.]
- **COVID cost less than expected** because two of our stocks, ______ and
  ______, rose sharply while the other eight fell about ______%. That
  cushion was luck: ______________________.
- **Concentration matters for biotechs.** At today's 10% holding, a trial
  failure costs less than one day's VaR. But the loss grows in a straight line
  with the holding, while VaR barely moves: at 50% the loss is $______ but VaR
  is only about $______. Above about ______% in one stock, a single failed
  trial would cost more than a 1-in-100 bad day.


## Recommendations
<!-- 2-4 concrete actions. E.g. which model to rely on, a concentration limit. -->

## Limitations
<!-- What this analysis can't tell you. Be honest; it shows judgement. -->
