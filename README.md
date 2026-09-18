# Private Pension Plan Financial Case

A Python-based retirement planning and portfolio construction case for a 45-year-old professional in Germany investing €250,000 for retirement at age 68.

**[View the case study](https://mujtababhutto.github.io/Private-Pension-Plan-Financial-Case/)**

## Overview

The case combines German statutory pension projections with a diversified private investment strategy. It estimates the client’s retirement-income gap, defines the capital required at retirement and tests a dynamic glide-path portfolio through Monte Carlo simulation, tax analysis and stress testing.

## Client case

| Profile | Assumption |
|---|---:|
| Current age | 45 |
| Retirement age | 68 |
| Investment horizon | 23 years |
| Current annual salary | €81,600 |
| Initial investment | €250,000 |
| Additional contributions | None |
| Private health insurance | €700 per month |
| Risk profile | Slightly risk-averse |

The retirement objective is 90% of final net salary plus private health insurance, supported by German statutory pension income and the private portfolio.

## Key results

| Retirement analysis | Result |
|---|---:|
| Annual income needed | €73,157 |
| Net statutory pension | €46,155 |
| Annual private funding gap | €27,003 |
| Required portfolio at a 4% planning rate | €675,070 |

| Portfolio projection | Result |
|---|---:|
| Median value at age 68 | €1,416,687 |
| 10th percentile | €973,167 |
| 90th percentile | €2,070,807 |
| Median CAGR | 7.83% |
| Outcomes above target before tax | 99.5% |
| Median after-tax value | €1,136,635 |
| Outcomes above target after tax | 97.2% |

## Portfolio strategy

The initial allocation is 50% equities, 40% bonds and 10% gold. Annual rebalancing gradually reduces equity exposure to 30% by retirement and raises bond exposure to 60%; gold remains at 10%.

The analysis begins with a broader ten-asset opportunity set. Historical risk, return and correlation evidence is used to compare global and emerging-market equities, infrastructure, listed property, euro fixed income, inflation-linked exposure and gold before selecting the five-asset investable portfolio.

| Holding | Starting weight | Portfolio role |
|---|---:|---|
| iShares Core MSCI World UCITS ETF | 40% | Global equity growth |
| iShares Global Infrastructure UCITS ETF | 10% | Real-asset equity exposure |
| iShares Core Euro Government Bond UCITS ETF | 20% | EUR duration and stability |
| iShares Core Euro Corporate Bond UCITS ETF | 20% | Investment-grade income |
| Invesco Physical Gold ETC | 10% | Inflation and crisis diversification |

## Analysis workflow

`run_full_analysis.py` is the single entry point for the complete workflow. The supporting modules keep the pension, portfolio and simulation logic separated so each component can be reviewed and tested independently.

The workflow covers:

- salary, pension-point, pension-tax and private-healthcare projections;
- retirement-income gap and required-capital calculations;
- ETF return, volatility, correlation, VaR and CVaR analysis;
- portfolio optimisation and the recommended glide path;
- 50,000 Monte Carlo accumulation paths with annual rebalancing;
- simplified German tax treatment; and
- adverse return scenarios and stress testing.

## Run the analysis

```bash
pip install -r requirements.txt
python run_full_analysis.py
```

To rebuild the website exhibits:

```bash
python analysis/build_exhibits.py
```

## Repository structure

```text
.
├── run_full_analysis.py             # Main entry point
├── config_file.py                   # Client, market and tax assumptions
├── pension_calculator.py            # Statutory pension projection
├── gap_analysis.py                  # Retirement-income gap and capital target
├── investment_metrics_calculator.py # Asset-level risk and return analysis
├── portfolio_optimizer.py           # Portfolio optimisation
├── glide_path_simulator.py          # Glide path and Monte Carlo simulation
├── stress_tests.py                  # Adverse scenarios
├── plotting_config.py               # Shared chart styling
├── analysis/                        # Website exhibit generation
├── data/                            # Historical return data
├── results/                         # Generated reports and simulation output
├── source/                          # Supporting case documents
└── docs/                            # GitHub Pages website
```

## Methodology notes

- Historical ETF returns inform the simulation parameters.
- The simulation assumes independent normally distributed returns.
- The tax calculation applies proportional rates to gains rather than transaction-level tax lots.
- Stress scenarios are sensitivity tests, not forecasts.
- Results depend on assumptions for inflation, pension policy, healthcare costs, returns and taxation.

## Disclaimer

This repository documents an educational financial-engineering case. It does not constitute personalised investment, tax or pension advice.
