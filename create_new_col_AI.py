"""
Taking two df, where df2 is a subset of df1 with only AI related rows. We update df1, adding a new column ["AI"]
df1["AI"] =  True only if that is present in df2 that is if it is related to AI

"""
import pandas as pd
import numpy as np
from utils import save_df


def filter_w_ai(df, outfolder="data/clean_data/", outformat="pkl", option="both", keyword_path="data/ai_keywords.csv"):
    """
    A function that will scan the dataframe and only keeps rows related to AI
    Parameters
    ----------
    df : dataframe
        the dataframe that needs filtering
    outfolder : str
        the folder where the output file should be saved
    keyword_path : str
        the path of the csv file containing all the keywords related to AI
    option : str
        Either "new_col", "new_df" or "both", depending if you need the small filtered df or the full df with a column
        True for AI or False if not related to AI
    outformat : str
        The output format, either pickle "pkl", or "csv"

    Returns nothing
    -------

    """
    df_main = df
    df_main["TXT"] = df_main["TI"] + " " + df_main["DE"] + " " + df_main["AB"]

    # Getting AI related keywords and adding them to a list
    keyword_csv = pd.read_csv(keyword_path, sep="\t", encoding="utf-8")
    # Put these keywords in a list and create a patter
    lst_ai = []
    for keyword in keyword_csv["Artificial Intelligence"]:
        lst_ai.append(keyword)
    # Creating a pattern of AI related keywords
    pattern = '|'.join([f'(?i){keyword}' for keyword in lst_ai])

    # Condition : Does the TXT contain one of the keyword?
    condition = df_main.TXT.str.contains(pattern, na=False)
    # We add a new column AI = True if it's AI related of False if not
    df_main['AI'] = np.where(condition, True, False)
    # We also create a new DB with only AI related rows
    df_filtered = df_main[condition].drop(columns=["AI"])

    columns_main = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'CN', 'PY', 'TXT', 'AI']
    columns_filtered = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'CN', 'PY', 'TXT']

    if option == "new_col" or option == "both":
        save_df(df_main, path=str(outfolder) + "full_data_AI_col." + str(outformat), typ=outformat,
                columns=columns_main)
    if option == "new_df" or option == "both":
        save_df(df_filtered, path=str(outfolder) + "full_data_filtered." + str(outformat), typ=outformat,
                columns=columns_filtered)

    # df_main.to_csv(out_path_ai_col, columns=columns_main, header=True, index=False, sep='\t')
    # df_filtered.to_csv(out_path_filtered, columns=columns_filtered, header=True, index=False,
    #                    sep='\t')
    # print(df_main.info())


if __name__ == "__main__":
    # Kevin // Comment, uncomment the right one.
    file_path_main = "data/clean_data/CA_full_data.pkl"
    out_path_filtered = "data/clean_data/CA_full_data_filtered.pkl"
    # out_path_ai_col = "data/clean_data/full_data_AI_col.pkl"

    # Laura
    # file_path_main = "data/clean_data/LoL_full_data.pkl"
    # out_path_filtered_laura = "data/clean_data/LoL_full_data_filtered.pkl"
    # out_path_ai_col_laura = "data/trash_db/LoL_full_data_AI_col.pkl"

    # Reading and adding a column TXT that is the aggregate of all text columns
    if file_path_main.split(".")[-1] == "csv":
        df = pd.read_csv(file_path_main, sep='\t', encoding='utf-8', index_col=False)
    elif file_path_main.split(".")[-1] == "pkl":
        df = pd.read_pickle(file_path_main)
    else:
        raise Exception("The input file is neither csv nor pickle")

    # Main function
    filter_w_ai(df, outfolder="data/clean_data/CA_", outformat="pkl", option="both")
