import pandas as pd
from gr import plot_all_numeric_columns

clean_files = [
    "compensation_clean.csv",
    "gross_output_clean.csv",
    "value_added_clean.csv",
    "employment_clean.csv"
]

# Save folder can be "." for current directory, or specify e.g., "plots"
plot_all_numeric_columns(clean_files, save_folder=".")