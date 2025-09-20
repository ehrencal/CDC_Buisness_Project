# graphs.py
"""Plotting helpers used by both pipelines. Uses seaborn + matplotlib for clean visuals."""

from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

sns.set(style="whitegrid", context="talk")

def save_line_plot(df: pd.DataFrame, title: str, ylabel: str, out_path: str,
                   top_n_legend: int = None, figsize=(12,6), markers=True):
    """
    df: index=Industry, columns=Year -> we will transpose and plot years on x axis
    top_n_legend: if provided, show only the top N series in legend (others faded) for readability
    """
    df_plot = df.T  # now index=Year, columns=Industry
    years = [str(x) for x in df_plot.index]

    plt.figure(figsize=figsize)
    # If top_n_legend provided, find top series by mean absolute value across time
    if top_n_legend is not None and top_n_legend < len(df_plot.columns):
        ranking = df.abs().mean(axis=1).sort_values(ascending=False)  # careful: df is Industries x years; we want mean across years per industry
        # compute mean across columns of original df (industries) => convert to series
        # We'll compute means properly:
        means = df.mean(axis=1).abs().sort_values(ascending=False)
        top_inds = means.index[:top_n_legend].tolist()
    else:
        top_inds = list(df.index)

    # Plot all series with low alpha
    for col in df_plot.columns:
        vals = df_plot[col].values
        if col in top_inds:
            if markers:
                plt.plot(years, vals, marker='o', linewidth=2.2, label=col)
            else:
                plt.plot(years, vals, linewidth=2.2, label=col)
        else:
            if markers:
                plt.plot(years, vals, marker='o', linewidth=1, alpha=0.25)
            else:
                plt.plot(years, vals, linewidth=1, alpha=0.25)

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    # If many legends, show only top_inds in legend (this keeps the legend readable)
    if top_n_legend:
        plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize='small')
    else:
        plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize='small', ncol=1)

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
