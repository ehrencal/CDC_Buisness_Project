#!/usr/bin/env python3
"""
pipeline_full.py
Full pipeline: clean, compute, save derived CSVs, and produce full-industry plots (many lines).
This script expects the four source files to be present in the same directory.
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import read_and_clean_csv, align_dataframes, compute_derived_metrics, ensure_output_dir

# Input filenames (must be in same folder where you run the script)
INPUT_FILES = {
    "compensation": "Space Economy Compensation by Industry.csv",
    "gross_output": "Real Gross Output by Industry.csv",
    "value_added": "Real Value Added by Industry.csv",   # optional
    "employment": "Space Economy Employment by Industry.csv"
}

OUT_DIR = "outputs/full"
ensure_output_dir(OUT_DIR)

sns.set(style="whitegrid")  # Seaborn style


def abbreviate_industry(name, max_words=4):
    """Abbreviate long industry names for legend."""
    words = name.strip().split()
    if len(words) > max_words:
        return ' '.join(words[:2]) + '...'  # keep first 2 words and add ellipsis
    return name.strip()


def save_line_plot(df, title, ylabel, out_path):
    """
    Plot a DataFrame (industries x years) as a line plot.
    Automatically abbreviates long legend labels.
    """
    df = df.copy()
    df.index = [abbreviate_industry(i) for i in df.index]

    plt.figure(figsize=(18, 10))  # larger figure for readability
    ax = sns.lineplot(data=df.T, marker='o', linewidth=2)

    ax.set_title(title, fontsize=22)
    ax.set_xlabel("Year", fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)

    # Legend outside plot
    ax.legend(title="Industry", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, title_fontsize=12)

    # Adjust layout to avoid warnings
    plt.tight_layout()
    plt.subplots_adjust(right=0.75, bottom=0.15, top=0.9)

    # Save figure
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()


def main():
    # Read available files
    dfs = {}
    for key, fname in INPUT_FILES.items():
        if Path(fname).exists():
            print(f"Reading {fname}")
            dfs[key] = read_and_clean_csv(fname)
        else:
            print(f"Warning: {fname} not found. Key '{key}' will be unavailable.")

    # Require at least compensation, employment, and one output measure
    if "compensation" not in dfs or "employment" not in dfs or (("gross_output" not in dfs) and ("value_added" not in dfs)):
        raise SystemExit("ERROR: Need compensation, employment, and either gross_output or value_added files present.")

    output_key = "gross_output" if "gross_output" in dfs else "value_added"

    # Align all three dfs
    subset = {k: dfs[k] for k in ["compensation", "employment", output_key]}
    subset_aligned, common_years = align_dataframes(subset)

    # Save cleaned CSVs for record
    for k, df in subset_aligned.items():
        df.to_csv(os.path.join(OUT_DIR, f"{k}_clean.csv"))

    # Compute derived metrics
    derived = compute_derived_metrics(subset_aligned["compensation"],
                                      subset_aligned["employment"],
                                      subset_aligned[output_key])

    # Save derived CSVs
    derived["labor_hoarding_diff"].to_csv(os.path.join(OUT_DIR, "labor_hoarding_diff_percent.csv"))
    derived["labor_hoarding_ratio"].to_csv(os.path.join(OUT_DIR, "labor_hoarding_ratio_percent.csv"))
    derived["wage_inflation"].to_csv(os.path.join(OUT_DIR, "wage_inflation_percent.csv"))
    derived["avg_comp"].to_csv(os.path.join(OUT_DIR, "avg_compensation_per_employee.csv"))
    derived["pct_emp"].to_csv(os.path.join(OUT_DIR, "pct_employment_change.csv"))
    derived["pct_output"].to_csv(os.path.join(OUT_DIR, "pct_output_change.csv"))

    # Produce plots (all industries)
    save_line_plot(derived["labor_hoarding_diff"],
                   title="Labor Hoarding (%ΔEmployment - %ΔOutput) — All Industries",
                   ylabel="Percentage points",
                   out_path=os.path.join(OUT_DIR, "labor_hoarding_diff_all.png"))

    save_line_plot(derived["labor_hoarding_ratio"],
                   title="Labor Hoarding Ratio ((1+ΔEmp)/(1+ΔOut)-1) — All Industries",
                   ylabel="Percent",
                   out_path=os.path.join(OUT_DIR, "labor_hoarding_ratio_all.png"))

    save_line_plot(derived["wage_inflation"],
                   title="Wage Inflation (YoY % change in avg compensation per employee) — All Industries",
                   ylabel="Percent",
                   out_path=os.path.join(OUT_DIR, "wage_inflation_all.png"))

    # Create summary CSV (mean/median across industries by year)
    summary = pd.DataFrame(index=common_years)
    summary["mean_pct_emp_change"] = derived["pct_emp"].mean(axis=0)
    summary["mean_pct_output_change"] = derived["pct_output"].mean(axis=0)
    summary["mean_labor_hoarding_diff"] = derived["labor_hoarding_diff"].mean(axis=0)
    summary["median_labor_hoarding_diff"] = derived["labor_hoarding_diff"].median(axis=0)
    summary["mean_wage_inflation_pct"] = derived["wage_inflation"].mean(axis=0)
    summary.to_csv(os.path.join(OUT_DIR, "summary_by_year.csv"))

    print("Full pipeline complete. Outputs in:", os.path.abspath(OUT_DIR))


if __name__ == "__main__":
    main()
