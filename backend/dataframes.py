import pandas as pd

# Helper function to clean CSVs
def load_and_clean_csv(filepath, skiprows=0):
    df_raw = pd.read_csv(filepath, skiprows=skiprows)
    return df_raw

# Load individual CSVs
employment_df = load_and_clean_csv('../data/Compensation_By_Industry.csv')
compensation_df = load_and_clean_csv('../data/Employment_By_Industry.csv')
real_output_df = load_and_clean_csv('../data/Real_Gross_Output_By_Industry.csv')
value_added_df = load_and_clean_csv('../data/Real_Value_Added_By_Industry.csv')
