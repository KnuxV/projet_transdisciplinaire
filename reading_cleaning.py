"""
Script which takes all txt files from a folder, convert them and save them in to csv file.
"""
import pandas as pd
import os
import sys
from utils import trim_py, country_name_fixing, save_df


def concat_df(root_dir_path):
    """

    Parameters
    ----------
    root_dir_path path
        folder path where are located all the text files used to create the concatenated db

    Returns
    -------
    dataframe
        the dataframe containing all the concatenated files
    """

    lst_of_df = []
    columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']
    # We explore the folder and its sub-folder looking for .txt to be read as dataframes
    for subdir, dirs, files in os.walk(root_dir_path):
        for file in files:
            file_path = subdir + '/' + file
            try:
                # Error bad lines = False to skip parsing errors
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False, )
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

                # Fixing C1 from Address to Country // Solving the UK problem
                df = country_name_fixing(df)
                df = trim_py(df, 2010, 2020)

                lst_of_df.append(df)
            except pd.errors.ParserError:
                print(file_path)

    #  Concatenation
    df_concat = pd.concat(lst_of_df)

    # Removing Duplicates
    df_concat = df_concat.drop_duplicates(['AB', 'TI'], keep='last')

    return df_concat


if __name__ == "__main__":
    # MODIFY root_dir and final_path here or add them as arguments
    root_dir = "data/raw/"
    # Laura root_dir
    root_dir_laura = "/home/kevin-main/Documents/Laura"
    final_path = 'data/clean_data/full_data.csv'
    final_path_pickle = 'data/clean_data/full_data.pkl'
    final_path_pickle_laura = 'data/clean_data/LoL_full_data.pkl'
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
        final_path = sys.argv[2]

    # Kevin
    # df = concat_df(root_dir)
    # save_df(df, final_path_pickle)

    # Laura
    df = concat_df(root_dir_laura)
    save_df(df, final_path_pickle_laura)

    print(df.PY.describe())
    print(df.info())
    print(df.CN.head(10))
