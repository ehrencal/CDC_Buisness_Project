import pandas as pd

# Original CSV files and cleaned output names
csv_files = [
    {"file": "Space Economy Compensation by Industry.csv", "clean_file": "compensation_clean.csv"},
    {"file": "Real Gross Output by Industry.csv", "clean_file": "gross_output_clean.csv"},
    {"file": "Real Value Added by Industry.csv", "clean_file": "value_added_clean.csv"},
    {"file": "Space Economy Employment by Industry.csv", "clean_file": "employment_clean.csv"},
]

for f in csv_files:
    # Skip first 5 rows, row 6 is header
    df = pd.read_csv(f["file"], skiprows=5)
    
    # Drop first column (index numbers) and rename column 2 as Industry
    df = df.iloc[:, 1:]
    df.rename(columns={df.columns[0]: "Industry"}, inplace=True)
    
    # Set industry as index
    df.set_index("Industry", inplace=True)
    
    # Replace '...' with NaN and convert all columns to numeric
    df.replace("...", pd.NA, inplace=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    
    # Save cleaned CSV
    df.to_csv(f["clean_file"])
    print(f"Saved cleaned CSV: {f['clean_file']}")

