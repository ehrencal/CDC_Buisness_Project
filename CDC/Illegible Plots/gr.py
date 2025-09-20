import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

def clean_df(df):
    """Ensure numeric data, drop rows that are all NaN"""
    df_clean = df.apply(pd.to_numeric, errors='coerce')
    df_clean = df_clean.dropna(how='all')
    return df_clean

def plot_all_numeric_columns(files, save_folder="."):
    for f in files:
        df = pd.read_csv(f, index_col=0)
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
        
        numeric_cols = df.columns.tolist()
        
        for col in numeric_cols:
            df_melted = df.reset_index().melt(id_vars="Industry", value_vars=[col],
                                             var_name="Year", value_name="Value")
            
            plt.figure(figsize=(14,7))
            ax = sns.lineplot(data=df_melted, x="Year", y="Value", hue="Industry", marker="o")
            ax.set_title(f"{col} Across Industries ({f})")
            ax.set_xlabel("Year")
            ax.set_ylabel(col)
            ax.legend(bbox_to_anchor=(1.05,1), loc='upper left')
            
            safe_name = str(col).replace(" ", "_").replace("/", "_")
            plt.savefig(f"{save_folder}/{f.split('.')[0]}_{safe_name}.png", bbox_inches='tight')
            plt.close()
            print(f"Saved plot for {col} from {f}")
