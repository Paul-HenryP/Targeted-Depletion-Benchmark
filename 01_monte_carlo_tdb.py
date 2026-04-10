"""
Targeted Depletion Benchmark (TDB) - Monte Carlo Simulations
Corresponds to Sections 4 and 5 of the paper.
This script generates Table 1 (Confidence Level Sensitivity) 
and Table 2 (Volatility Drag Isolated).
"""

import numpy as np
import pandas as pd

# Hardcoded seed for academic reproducibility
np.random.seed(42)  

# --- MODEL PARAMETERS (Section 4.1) ---
TARGET_WEALTH = 810848
COASTING_YEARS = 35
ANNUAL_SAVINGS_LIMIT = 15000
BASE_MU = 0.07     # 7% real return arithmetic mean
BASE_SIGMA = 0.15  # 15% volatility (Standard equity portfolio)

def calculate_stochastic_tdb(target_w, years, mu, sigma, confidence_level=0.95, trials=100000):
    """
    Finds the required TDB starting wealth to reach the target wealth 
    with a given probability of success. Assumes log-normal distribution.
    """
    # Simulate return paths
    daily_returns = np.random.normal(mu, sigma, (trials, years))
    
    # Calculate the cumulative growth factor of $1 over the time period
    growth_factors = np.prod(1 + daily_returns, axis=1)
    
    # Find the lower bound growth factor corresponding to the failure rate limit
    percentile_target = (1 - confidence_level) * 100
    worst_case_growth = np.percentile(growth_factors, percentile_target)
    
    # Calculate required initial capital based on that worst-case growth path
    stochastic_tdb = target_w / worst_case_growth
    
    return stochastic_tdb

if __name__ == "__main__":
    # ==========================================
    # TABLE 1: Confidence Interval Sensitivity
    # ==========================================
    confidence_levels = [0.50, 0.70, 0.80, 0.90, 0.95]
    results_conf = []

    for conf in confidence_levels:
        tdb = calculate_stochastic_tdb(TARGET_WEALTH, COASTING_YEARS, BASE_MU, BASE_SIGMA, conf)
        years_labor = tdb / ANNUAL_SAVINGS_LIMIT
        results_conf.append({
            "Confidence Level": f"{conf*100:.0f}%",
            "Required TDB": tdb,
            "Years of Labor ($15k/yr)": years_labor
        })

    df_conf = pd.DataFrame(results_conf)
    df_conf['Required TDB'] = df_conf['Required TDB'].apply(lambda x: f"${x:,.0f}")
    df_conf['Years of Labor ($15k/yr)'] = df_conf['Years of Labor ($15k/yr)'].apply(lambda x: f"{x:.1f} yrs")

    print("--- TABLE 1: TDB by Target Confidence Level ---")
    print(df_conf.to_string(index=False))
    print("\n")

    # ==========================================
    # TABLE 2: Volatility (Sequence Risk) Sensitivity
    # ==========================================
    volatilities = [0.05, 0.10, 0.15, 0.20]
    vol_labels = ["Low (5%)", "Moderate (10%)", "Standard (15%)", "High (20%)"]
    results_vol = []

    for sigma, label in zip(volatilities, vol_labels):
        tdb = calculate_stochastic_tdb(TARGET_WEALTH, COASTING_YEARS, BASE_MU, sigma, confidence_level=0.90)
        results_vol.append({
            "Volatility Profile (\u03C3)": label,
            "Required TDB (90% Conf)": tdb
        })

    df_vol = pd.DataFrame(results_vol)
    df_vol['Required TDB (90% Conf)'] = df_vol['Required TDB (90% Conf)'].apply(lambda x: f"${x:,.0f}")

    print("--- TABLE 2: Volatility Drag on 90% Confidence TDB (Constant \u03BC = 0.07) ---")
    print(df_vol.to_string(index=False))