import pandas as pd

if __name__ == "__main__":
    file_path = "data/clean_data/full_data.csv"
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False)

    # Only keeping main languages to filter wrongly parsed rows
    lst_of_language = ["English", "Spanish", "Portugese", "Chinese", "French", "Russian", "German",
                       "Korean", "Turkish",
                       "Polish", "Czech", "Japanese", "Italian"]
    condition = df.LA.isin(lst_of_language)
    df = df[condition]

    # fixing countries
    df['C1'] = df['C1'].apply(lambda x: x.split(", ")[-1] if "USA" not in x else "United States")
    df['C1'] = df['C1'].replace(['Peoples R China'], 'China')

    # Fixing Year of Publication
    condition_year = df.PY > 2009
    df = df[condition_year]

    # Dropping duplicated
    print(df.duplicated().sum())
    df = df.drop_duplicates()

    columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']
    df.to_csv("data/clean_data/full_data_fixed_language_country_year_no_dups.csv", columns=columns, header=True,
              index=False, sep='\t')
