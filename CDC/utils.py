# utils.py
"""Helpers for cleaning the four CSVs and computing derived labor/wage metrics."""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import os

def read_and_clean_csv(path: str, skiprows: int = 5) -> pd.DataFrame:
    """
    Read CSV according to the spreadsheet layout you described:
    - skiprows: number of rows to skip at top (random text)
    - row after skiprows is assumed to be the header (years + first label column)
    - drop first column (index numbers)
    - second column becomes 'Industry' (index)
    - replace '...' and similar with NaN and coerce numeric columns
    """
    df = pd.read_csv(path, skiprows=skiprows)
    # Drop the very first column (index numbers)
    df = df.iloc[:, 1:]
    # Rename the first remaining column to 'Industry' if it's not already
    df.rename(columns={df.columns[0]: "Industry"}, inplace=True)
    # Set industry as index
    df.set_index("Industry", inplace=True)
    # Replace string placeholders with NA
    df.replace(["...", "..", ".", "NA", "na", ""], pd.NA, inplace=True)
    # Attempt numeric conversion for all other columns
    df = df.apply(pd.to_numeric, errors="coerce")
    # Drop rows that are completely NA
    df = df.dropna(how="all")
    return df

def align_dataframes(dfs: Dict[str, pd.DataFrame]) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    """
    Intersect industries and years across provided dataframes and return the aligned dict + common_years list.
    Expects keys like 'compensation','employment','gross_output','value_added'.
    """
    # find common industries
    keys = list(dfs.keys())
    industries_sets = [set(dfs[k].index) for k in keys]
    common_industries = sorted(set.intersection(*industries_sets))
    if len(common_industries) == 0:
        raise ValueError("No common industries across the provided files.")
    # align each df to those industries
    for k in keys:
        dfs[k] = dfs[k].loc[common_industries]

    # intersect columns (years)
    year_sets = [set(dfs[k].columns) for k in keys]
    common_years = [c for c in dfs[keys[0]].columns if all(c in dfs[k].columns for k in keys)]
    if len(common_years) == 0:
        raise ValueError("No common years across the provided files.")
    for k in keys:
        dfs[k] = dfs[k][common_years]

    return dfs, common_years

def compute_derived_metrics(comp: pd.DataFrame, emp: pd.DataFrame, output: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Given cleaned compensation, employment, and output dataframes (indexed by Industry, columns = years),
    compute:
      - avg_comp: average compensation per employee (comp / emp)
      - wage_inflation: YoY % change in avg_comp
      - pct_emp: employment YoY % change
      - pct_output: output YoY % change
      - labor_hoarding_diff: pct_emp - pct_output (percentage point diff)
      - labor_hoarding_ratio: ((1+Δemp) / (1+Δout) -1) * 100 (percent)
    Returns a dict with these DataFrames (industries x years; note first year will be NaN for percent-change metrics).
    """
    comp = comp.copy()
    emp = emp.copy()
    output = output.copy()

    # Average compensation per employee
    avg_comp = comp.divide(emp).replace([np.inf, -np.inf], np.nan)

    # YoY percent changes
    wage_inflation = avg_comp.pct_change(axis=1) * 100  # percent
    pct_emp = emp.pct_change(axis=1) * 100
    pct_output = output.pct_change(axis=1) * 100

    # Labor hoarding measures
    labor_hoarding_diff = pct_emp - pct_output  # percentage points
    emp_frac_change = pct_emp / 100.0
    output_frac_change = pct_output / 100.0
    labor_hoarding_ratio = ((1 + emp_frac_change) / (1 + output_frac_change) - 1) * 100.0

    return {
        "avg_comp": avg_comp,
        "wage_inflation": wage_inflation,
        "pct_emp": pct_emp,
        "pct_output": pct_output,
        "labor_hoarding_diff": labor_hoarding_diff,
        "labor_hoarding_ratio": labor_hoarding_ratio
    }

def ensure_output_dir(path: str):
    os.makedirs(path, exist_ok=True)
