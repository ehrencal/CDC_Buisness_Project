#!/usr/bin/env python3
"""
multi_metric_plots.py
Produce multi-panel figures combining multiple derived metrics (labor hoarding and wage inflation)
for all industries. Uses cleaned and derived CSVs.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")  # Seaborn style

# Folder containing cleaned/derived CSVs
INPUT_DIR = "outputs/full"
OUT_FILE = os.path.join(INPUT_DIR, "multi_metric_all_industries.png")


def abbreviate_industry(name, max_words=4):
    """Abbreviate long industry names for legend."""
    words = name.strip().split()
    if len(words) > max_words:
        return ' '.join(words[:2]) + '...'  # first 2 words + ellipsis
    return name.strip()


def load_metric_csv(filename):
    """Load a CSV from INPUT_DIR and abbreviate industry names."""
    path = os.path.join(INPUT_DIR, filename)
    df = pd.read_csv(path, index_col=0)
    df.index = [abbreviate_industry(i) for i in df.index]
    return df


def plot_multi_metric(metrics, titles, ylabels, out_file):
    """
    Create a multi-panel figure for multiple metrics.
    
    metrics: list of DataFrames (industries x years)
    titles: list of subplot titles
    ylabels: list of y-axis labels
    """
    n_metrics = len(metrics)
    fig, axes = plt.subplots(n_metrics, 1, figsize=(20, 12), sharex=True)

    if n_metrics == 1:
        axes = [axes]  # ensure iterable

    for ax, df, title, ylabel in zip(axes, metrics, titles, ylabels):
        df_T = df.T  # transpose for plotting (years x industries)
        sns.lineplot(data=df_T, ax=ax, marker='o', linewidth=1.8)
        ax.set_title(title, fontsize=18)
        ax.set_ylabel(ylabel, fontsize=14)
        ax.grid(True)
    
    # Shared x-axis label
    axes[-1].set_xlabel("Year", fontsize=14)

    # Single legend for all subplots
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title="Industry", bbox_to_anchor=(1.02, 0.9), loc='upper left',
               fontsize=10, title_fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(right=0.75, hspace=0.3, bottom=0.15, top=0.95)

    # Save high-resolution figure
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Multi-metric figure saved to: {out_file}")


def main():
    # Load derived CSVs
    labor_hoarding_diff = load_metric_csv("labor_hoarding_diff_percent.csv")
    labor_hoarding_ratio = load_metric_csv("labor_hoarding_ratio_percent.csv")
    wage_inflation = load_metric_csv("wage_inflation_percent.csv")

    metrics = [labor_hoarding_diff, labor_hoarding_ratio, wage_inflation]
    titles = ["Labor Hoarding (%ΔEmployment - %ΔOutput)", 
              "Labor Hoarding Ratio ((1+ΔEmp)/(1+ΔOut)-1)", 
              "Wage Inflation (YoY % change in avg compensation per employee)"]
    ylabels = ["Percentage points", "Percent", "Percent"]

    plot_multi_metric(metrics, titles, ylabels, OUT_FILE)


if __name__ == "__main__":
    main()
