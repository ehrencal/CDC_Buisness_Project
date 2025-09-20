import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- File names ---
real_file = "Space Economy Real Value Added by Industry.csv"
nominal_file = "Space Economy Value Added by Industry.csv"

# --- Read and clean CSV ---
def read_csv_clean(fname):
    df = pd.read_csv(fname, header=None)
    df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
    numeric_cols = [col for col in df.columns if pd.to_numeric(df[col], errors='coerce').notna().any()]
    first_numeric_col = numeric_cols[0]
    for col in df.columns[first_numeric_col:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors='coerce')
    return df, first_numeric_col

# --- Read datasets ---
real_df, real_start_col = read_csv_clean(real_file)
nominal_df, nominal_start_col = read_csv_clean(nominal_file)

# --- Total row index: 11th from bottom ---
total_row_idx_real = len(real_df) - 11
total_row_idx_nominal = len(nominal_df) - 11

# --- Extract totals: ignore any initial non-numeric entries ---
real_total = real_df.iloc[total_row_idx_real, real_start_col:].dropna().values
real_total = real_total[-12:]  # take last 12 values (2012-2023)

nominal_total = nominal_df.iloc[total_row_idx_nominal, nominal_start_col:].dropna().values
nominal_total = nominal_total[-12:]  # last 12 values

# --- X-axis for actual data (2012-2023) ---
years_actual = list(range(2012, 2024))  # 12 years

# --- Function to plot Real/Nominal GDP ---
def plot_value_added(real, nominal, years):
    plt.figure(figsize=(14, 7))
    
    # Plot actual data points
    plt.plot(years, real, marker='o', label='Real ($M)', color='blue')
    plt.plot(years, nominal, marker='o', label='Nominal ($M)', color='red')
    
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Value ($M)", fontsize=12)
    plt.xticks(years)  # show all years
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=10, loc='best')
    
    # Abbreviate y-axis labels
    plt.gca().get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'{int(x/1e3)}k' if x >= 1e3 else int(x))
    )
    
    plt.title("Space Economy: Real vs Nominal Value Added", fontsize=16)
    plt.tight_layout()
    plt.savefig("space_economy_value_added.png")
    plt.show()
    print("Plot saved as: space_economy_value_added.png")

# --- Plot the graph ---
plot_value_added(real_total, nominal_total, years_actual)
