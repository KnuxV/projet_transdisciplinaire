import pandas as pd
import os

root_dir = "data/raw/"


def concat_df(path):
    """

    :param path:
    :return:
    """
    lst_of_df = []
    # We explore the folder and its subfolder looking for .txt to be read as dataframes
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = subdir + '/' + file
            try:
                # Error bad lines = False to skip parsing errors on somes lines
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False)
                # we keep only a handful of useful variables, to avoid bugs, we only keep the file if our 8 variables
                # are present.
                columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']
                set_columns = set(columns)
                if set_columns.issubset(set(df.columns)):
                    # making sure to only keep rows that have the proper columns
                    df = df[['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']]
                else:
                    continue

                # We need to remove NaN values
                df = df.dropna()
                # C1 the Author address is changed to keep only the country
                # df['C1'] = df['C1'].apply(lambda x: x.split(', ')[-1])
                lst_of_df.append(df)
            except pd.errors.ParserError:
                print(file_path)

    df_concat = pd.concat(lst_of_df)
    df_concat.to_csv("data/clean_data/full_data.csv", columns=columns, header=True, index=False, sep='\t')
    return df_concat


df = concat_df(root_dir)
print(df.head())
print(df.info())
