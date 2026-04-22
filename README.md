# The Targeted Depletion Benchmark (TDB)

This repository contains the Python source code and simulation models for the paper:
**"The Targeted Depletion Benchmark (TDB): A Stochastic Optimization Model for Labor Cessation and Sequence Risk"** by Paul-Henry Paltmann.

Read the full paper on SSRN: https://dx.doi.org/10.2139/ssrn.6260638

## Overview

Traditional retirement heuristics mandate continuous capital accumulation until decumulation, exposing investors to sequence of returns risk (SRR) while over-taxing their lifetime labor supply. This repository contains models that calculate the exact mathematical threshold (W_TDB\*) required to safely cease savings early ("Coasting") by utilizing log-normal Monte Carlo simulations and overlapping historical backtests using Robert Shiller's market data.

## Repository Structure

- `src/01_monte_carlo_tdb.py`: Simulates 100,000 geometric return paths to calculate required initial capital across different confidence intervals and asset allocation volatilities. Generates **Table 1** and **Table 2** from the paper.
- `src/02_shiller_backtest.py`: Fetches historical Shiller data (1872-1989) and runs a 35-year overlapping cohort backtest. Applies the _Dynamic Unification Framework_ (Endogenous Yields, Blanchett's Spending Smile, and the Human Capital Margin Call). Generates **Table 3**.

## Requirements

To run these models locally, you need Python 3.8+ and the following libraries:
`pip install pandas numpy requests`

## Usage

Run the Monte Carlo simulations (Section 4 & 5):
`python src/01_monte_carlo_tdb.py`

Run the Shiller Historical Backtest (Section 6):
`python src/02_shiller_backtest.py`

## Data Source

The historical backtest dynamically fetches Robert Shiller's S&P 500 dataset from the standard open-source datasets repository (`https://raw.githubusercontent.com/datasets/s-and-p-500/master/data/data.csv`).
