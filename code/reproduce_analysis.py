#!/usr/bin/env python3
"""
Reproduce the core computations reported in the manuscript:
- Build inter-event intervals from milestone nodes (Life + Civilization)
- Fit an exponential decay model in log-space: ln(Δt_n) = a + b*n
- Produce the model-implied monitoring / transition window (as in Forecast_Window)

Input data: CSVs exported from Supplementary_Data_1_Milestone_Database.xlsx
Outputs: results tables in ./outputs
"""
from __future__ import annotations
import os
import math
import pandas as pd
import numpy as np

try:
    import statsmodels.api as sm
except ImportError as e:
    raise SystemExit("Missing dependency statsmodels. Install with: pip install -r requirements.txt") from e

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(ROOT), "data")
OUT = os.path.join(os.path.dirname(ROOT), "outputs")
os.makedirs(OUT, exist_ok=True)

def fit_decay(intervals: pd.DataFrame, seq_name: str) -> dict:
    """
    intervals must include: Log_Interval_ln and an ordered row index corresponding to n=1..N
    """
    y = intervals["Log_Interval_ln"].astype(float).to_numpy()
    n = np.arange(1, len(y)+1, dtype=float)
    X = sm.add_constant(n)  # [1, n]
    model = sm.OLS(y, X).fit()
    a = float(model.params[0])
    b = float(model.params[1])
    r = math.exp(b)  # decay ratio per step (if b<0 then r<1)
    return {
        "Sequence": seq_name,
        "N_intervals": int(len(y)),
        "Intercept_ln_dt0": a,
        "Slope_ln_r": b,
        "Decay_r": r,
        "R_squared": float(model.rsquared)
    }

def main():
    civ_int = pd.read_csv(os.path.join(DATA, "civilization_intervals.csv"))
    life_int = pd.read_csv(os.path.join(DATA, "life_intervals.csv"))

    # Ensure order is preserved as provided
    civ_fit = fit_decay(civ_int, "Civilization")
    life_fit = fit_decay(life_int, "Life")

    fits = pd.DataFrame([civ_fit, life_fit])
    fits.to_csv(os.path.join(OUT, "recomputed_model_fit.csv"), index=False)

    # Simple check: compare to provided Model_Fit sheet (if present)
    provided = pd.read_csv(os.path.join(DATA, "model_fit.csv"))
    check = provided.merge(fits, on="Sequence", suffixes=("_provided", "_recomputed"), how="outer")
    check.to_csv(os.path.join(OUT, "model_fit_comparison.csv"), index=False)

    # Export a combined "analysis-ready" dataset
    civ_int2 = civ_int.copy()
    civ_int2["Sequence"] = "Civilization"
    civ_int2["n"] = np.arange(1, len(civ_int2)+1)
    life_int2 = life_int.copy()
    life_int2["Sequence"] = "Life"
    life_int2["n"] = np.arange(1, len(life_int2)+1)
    combined = pd.concat([civ_int2, life_int2], ignore_index=True)
    combined.to_csv(os.path.join(OUT, "analysis_ready_intervals.csv"), index=False)

    print("Done. Outputs written to:", OUT)

if __name__ == "__main__":
    main()
