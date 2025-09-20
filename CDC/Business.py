import pandas as pd

csv_configs = [
    {'file': 'Space Economy Compensation by Industry.csv', 'start_row': 6, 'end_row': 101},  
    {'file': 'Real Gross Output by Industry.csv', 'start_row': 6, 'end_row': 101},  
    {'file': 'Real Value Added by Industry.csv', 'start_row': 6, 'end_row': 101},  
    {'file': 'Space Economy Employment by Industry.csv', 'start_row': 6, 'end_row': 101}, 
]

file_rows_dict = {}

for config in csv_configs:
    file = config['file']
    start = config['start_row']
    end = config['end_row']
    
    df = pd.read_csv(file)
    df = df.iloc[start:end + 1]
    df = df.iloc[:, 2:14]
    df = df.apply(pd.to_numeric, errors='coerce')
    rows_as_2d_arrays = [[row.tolist()] for _, row in df.iterrows()]
    file_rows_dict[file] = rows_as_2d_arrays

first_file = csv_configs[0]['file']
second_file = csv_configs[1]['file']
third_file = csv_configs[2]['file']
fourth_file = csv_configs[3]['file']
print(f"2D arrays for {first_file}:")
for arr in file_rows_dict[first_file]:
    print(arr)
print(f"\n2D arrays for {second_file}:")
for arr in file_rows_dict[second_file]:
    print(arr)
print(f"\n2D arrays for {third_file}:")
for arr in file_rows_dict[third_file]:
    print(arr)
print(f"\n2D arrays for {fourth_file}:")
for arr in file_rows_dict[fourth_file]:
    print(arr)