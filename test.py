import pandas as pd

file_path = "data/clean_data/full_data.csv"
df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False)

print(df.PY.describe())
print(df.info())

# Year of publication 2010-2020
condition_year = df.PY.between(2010, 2020, inclusive="both")
df = df[condition_year]

print(df.PY.describe())
print(df.info())