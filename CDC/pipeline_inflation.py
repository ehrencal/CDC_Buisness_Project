import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- File names ---
real_file = "Space Economy Real Value Added by Industry.csv"
nominal_file = "Space Economy Value Added by Industry.csv"

# --- Read and clean CSV ---
def read_csv_clean(fname):
    df = pd.read_csv(fname, header=None)
    # Strip strings
    df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
    # Detect first numeric column dynamically
    numeric_cols = [col for col in df.columns if pd.to_numeric(df[col], errors='coerce').notna().any()]
    first_numeric_col = numeric_cols[0]
    # Convert numeric columns to float
    for col in df.columns[first_numeric_col:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors='coerce')
    return df, first_numeric_col

# --- Read datasets ---
real_df, real_start_col = read_csv_clean(real_file)
nominal_df, nominal_start_col = read_csv_clean(nominal_file)

# --- Total row index (11th from bottom) ---
total_row_idx_real = len(real_df) - 11
total_row_idx_nominal = len(nominal_df) - 11

# --- Extract totals, skip invalid leading values ---
real_total = real_df.iloc[total_row_idx_real, real_start_col:].values[2:]       # skip first 2 invalid
nominal_total = nominal_df.iloc[total_row_idx_nominal, nominal_start_col:].values[2:]

# --- Years ---
years_actual = list(range(2012, 2024))  # 2012 to 2023 inclusive

# --- Calculate GDP Deflator and Inflation ---
# GDP Deflator = (Nominal / Real) * 100
gdp_deflator = (nominal_total / real_total) * 100

# Year-over-Year Inflation = % change in GDP deflator
inflation = np.diff(gdp_deflator) / gdp_deflator[:-1] * 100

# Years for inflation (one less than total)
inflation_years = years_actual[1:]

# --- Debug check ---
print("[DEBUG] GDP Deflator:", gdp_deflator)
print("[DEBUG] Inflation (% YoY):", inflation)

# --- Plot GDP Deflator ---
plt.figure(figsize=(12, 6))
plt.plot(years_actual, gdp_deflator, marker='o', color='purple', label='GDP Deflator')
plt.xlabel("Year", fontsize=12)
plt.ylabel("GDP Deflator (Index, 100=Base)", fontsize=12)
plt.title("Space Economy GDP Deflator (2012–2023)", fontsize=14)
plt.xticks(years_actual, rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("space_economy_gdp_deflator.png")
plt.show()
print("Plot saved as: space_economy_gdp_deflator.png")

# --- Plot Inflation ---
plt.figure(figsize=(12, 6))
plt.plot(inflation_years, inflation, marker='o', color='orange', label='YoY Inflation (%)')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Inflation (%)", fontsize=12)
plt.title("Space Economy Implied Inflation (2013–2023)", fontsize=14)
plt.xticks(inflation_years, rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("space_economy_inflation.png")
plt.show()
print("Plot saved as: space_economy_inflation.png")
