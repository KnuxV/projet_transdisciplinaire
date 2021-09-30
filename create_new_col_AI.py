"""
Taking two df, where df2 is a subset of df1 with only AI related rows. We update df1, adding a new column ["AI"]
df1["AI"] =  True only if that is present in df2 that is if it is related to AI

"""
import pandas as pd
import numpy as np


if __name__ == "__main__":
    file_path_main = "data/clean_data/full_data.csv"
    out_path_filtered = "data/clean_data/full_data_filtered.csv"
    out_path_ai_col = "data/clean_data/full_data_AI_col.csv"

    # Reading and adding a column TXT that is the aggregate of all text columns
    df_main = pd.read_csv(file_path_main, sep='\t', encoding='utf-8', index_col=False)
    df_main["TXT"] = df_main["TI"] + " " + df_main["DE"] + " " + df_main["AB"]

    # Getting AI related keywords and adding them to a list
    keyword_csv = pd.read_csv("data/ai_keywords.csv", sep="\t", encoding="utf-8")
    # Put these keywords in a list and create a patter
    lst_ai = []
    for keyword in keyword_csv["Artificial Intelligence"]:
        lst_ai.append(keyword)
    # Creating a pattern of AI related keywords
    pattern = '|'.join([f'(?i){keyword}' for keyword in lst_ai])

    # Condition : Does the TXT coutain one of the keyword?
    condition = df_main.TXT.str.contains(pattern, na=False)
    # We add a new column AI = True if it's AI related of False if not
    df_main['AI'] = np.where(condition, True, False)
    # We also create a new DB with only AI related rows
    df_filtered = df_main[condition].drop(columns=["AI"])

    columns_main = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY', 'TXT', 'AI']
    columns_filtered = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY', 'TXT']

    df_main.to_csv(out_path_ai_col, columns=columns_main, header=True, index=False, sep='\t')
    df_filtered.to_csv(out_path_filtered, columns=columns_filtered, header=True, index=False,
                       sep='\t')
    print(df_main.info())
