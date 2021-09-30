import pandas as pd
import os
import sys


def concat_df(root_dir_path, lst_of_cols):
    """

    :param lst_of_cols:
    :param root_dir_path:
    :return:
    """
    lst_of_df = []
    columns = lst_of_cols
    # We explore the folder and its sub-folder looking for .txt to be read as dataframes
    for subdir, dirs, files in os.walk(root_dir_path):
        for file in files:
            file_path = subdir + '/' + file
            try:
                # Error bad lines = False to skip parsing errors
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False)
                # we keep only a handful of useful variables, to avoid bugs, we only keep the file if our 8 variables
                # are present.

                set_columns = set(columns)
                if set_columns.issubset(set(df.columns)):
                    # making sure to only keep rows that have the proper columns
                    df = df[['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']]
                else:
                    continue

                # We need to remove NaN values
                df = df.dropna()

                # Language = English Only
                condition_language = df.LA == "English"
                df = df[condition_language]

                # # Year of publication 2010-2020
                # condition_year = df.PY.between(2010, 2020, inclusive="both")
                # df = df[condition_year]

                # Fixing C1 from Address to Country // Solving the UK problem
                df['C1'] = df['C1'].apply(lambda x: x.split(", ")[-1] if "USA" not in x else "United States")
                df['C1'] = df['C1'].replace(['Peoples R China'], 'China')
                df['C1'] = df['C1'].replace(['England'], 'United Kingdom')
                df['C1'] = df['C1'].replace(['Scotland'], 'United Kingdom')
                df['C1'] = df['C1'].replace(['Wales'], 'United Kingdom')
                df['C1'] = df['C1'].replace(['Northen Ireland'], 'United Kingdom')

                lst_of_df.append(df)
            except pd.errors.ParserError:
                print(file_path)

    #  Concatenation
    df_concat = pd.concat(lst_of_df)

    # Removing Duplicates
    print(df_concat.duplicated().sum())
    df_concat = df_concat.drop_duplicates()

    return df_concat


def save_df_to_csv(df, path, cols, header=True, index=False, sep="\t"):
    df.to_csv(path, columns=cols, header=header, index=index, sep=sep)


def trim_py(df, start_year, end_year, inclusive="both"):
    condition_year = df.PY.between(start_year, end_year, inclusive=inclusive)
    df = df[condition_year]
    return df


if __name__ == "__main__":
    # MODIFY root_dir and final_path here or add them as arguments
    root_dir = "data/raw/"
    final_path = 'data/clean_data/full_data.csv'
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
        final_path = sys.argv[2]

    columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']
    df = concat_df(root_dir, columns)

    save_df_to_csv(df, final_path, columns)

    # For some obscure reasons, we can't trim the initial df with year restrictions (can't compare int and string
    # error), so we save the db and reload it and it works....
    df = pd.read_csv("data/clean_data/full_data.csv", sep="\t", encoding="utf-8", index_col=False)
    df_final = trim_py(df, 2010, 2020, "both")
    save_df_to_csv(df, final_path, columns)

