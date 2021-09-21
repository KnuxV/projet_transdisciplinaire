import pandas as pd

file_path = "data/clean_data/full_data_fixed_language_country_year_no_dups.csv"
df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False)

print(df.info())