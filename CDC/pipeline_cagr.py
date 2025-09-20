import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text  # pip install adjustText

# ---------------------------
# 1. Load CSVs
# ---------------------------
real_file = r"CDC\Space Economy Real Value Added by Industry.csv"
employment_file = r"CDC\Space Economy Employment by Industry.csv"

def read_csv_clean(fname):
    df = pd.read_csv(fname, header=None)
    # Strip strings
    df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
    return df

real_df = read_csv_clean(real_file)
emp_df = read_csv_clean(employment_file)

# ---------------------------
# 2. Extract industry names
# ---------------------------
industry_labels = real_df.iloc[:, 1]  # column 2 has industry names

# ---------------------------
# 3. Compute CAGR
# ---------------------------
def compute_cagr(series):
    series_numeric = pd.to_numeric(series, errors='coerce')
    series_clean = series_numeric.dropna()
    if len(series_clean) < 2:
        return pd.NA
    first = series_clean.iloc[0]
    last = series_clean.iloc[-1]
    n = len(series_clean) - 1
    if first <= 0 or last <= 0:
        return pd.NA
    return ((last / first) ** (1 / n) - 1) * 100  # % CAGR

real_cagr = real_df.iloc[:, 2:].apply(compute_cagr, axis=1)
emp_cagr = emp_df.iloc[:, 2:].apply(compute_cagr, axis=1)

# ---------------------------
# 4. Filter out invalid values
# ---------------------------
valid_mask = (~real_cagr.isna()) & (~emp_cagr.isna()) & (emp_cagr > -100)
real_cagr = real_cagr[valid_mask]
emp_cagr = emp_cagr[valid_mask]
industry_labels_filtered = industry_labels[valid_mask]

# ---------------------------
# 5. Plot scatter
# ---------------------------
plt.figure(figsize=(14, 10))
plt.scatter(emp_cagr, real_cagr, s=150, color='skyblue')

plt.xlabel("Employment CAGR (%)", fontsize=14)
plt.ylabel("Real Value Added CAGR (%)", fontsize=14)
plt.title("Space Economy: Real Output vs Employment CAGR (2012-2023)", fontsize=16)

# Add industry labels
texts = []
for x, y, label in zip(emp_cagr, real_cagr, industry_labels_filtered):
    texts.append(plt.text(x, y, label, fontsize=10))

# Adjust text to reduce overlap
adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("scatter_cagr_labeled.png")
plt.show()
