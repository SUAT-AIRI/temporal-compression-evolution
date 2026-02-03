# Milestone database, derived intervals, and analysis code (double-blind package)

This repository contains the milestone database and reproducibility materials for the manuscript:

**"Civilizational Dynamics and the Evolution of Life Based on an Exponential Decay Model"**

## Contents
- `data/Supplementary_Data_1_Milestone_Database.xlsx` — master spreadsheet (nodes, provenance, intervals, model fit, forecast window)
- `data/*.csv` — CSV exports of the main sheets (nodes, intervals, model fit, forecast window)
- `code/reproduce_analysis.py` — minimal script to recompute the log-linear decay fit from the provided interval tables
- `code/requirements.txt` — Python dependencies
- `CITATION.cff` — citation metadata
- `zenodo.json` — suggested Zenodo metadata (edit DOI/title/version as needed)

## Data description (high level)
Two milestone sequences are provided:
- **Life evolution nodes** (14 nodes) and derived inter-event intervals (13 intervals)
- **Civilization nodes** (14 nodes) and derived inter-event intervals (13 intervals)

For each interval, the dataset includes:
- `Interval_Delta_t` (years BP)
- `Log_Interval_ln` = ln(Interval_Delta_t)

**BP convention:** the spreadsheet uses BP relative to **2025 CE** (i.e., BP = 2025 - calendar_year for CE years; for BCE years, convert to astronomical year numbering before transformation if needed).
The sheet also records lower/upper bounds and a median for uncertain dates.

## Reproducibility
From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
python code/reproduce_analysis.py
```

Outputs are written to `outputs/`.

## License
Recommended: **Creative Commons Attribution 4.0 International (CC BY 4.0)** for data and code.

## Notes for double-blind review
If required by the journal, deposit on Zenodo with **Embargoed** (or Restricted) access, reserve a DOI, and share the DOI in the Data Availability statement without revealing author identities in the manuscript files.
