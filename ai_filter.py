import pandas as pd
import re
import spacy
"""
Create a new column that is the aggregation of Document Title, Abstract and Keywords
Then apply a filter looking for articles relevant to artificial intelligence 
"""
file_path = "data/clean_data/full_data_fixed_language_country_year_no_dups.csv"

if __name__ == "__main__":
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False)
    txt_col = ["TI", "DE", "AB"]
    df["TXT"] = df["TI"] + " " + df["DE"] + " " + df["AB"]
    # Get the list of keywords related to AI only
    keyword_csv = pd.read_csv("data/ai_keywords.csv", sep="\t", encoding="utf-8")
    # Put these keywords in a list and create a patter
    lst_ai = []
    for keyword in keyword_csv["Artificial Intelligence"]:
        lst_ai.append(keyword)

    pattern = '|'.join([f'(?i){keyword}' for keyword in lst_ai])

    condition = df.TXT.str.contains(pattern, na=False)
    df = df[condition]

    columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY', 'TXT']
    df.to_csv("data/clean_data/full_data_filtered.csv", columns=columns, header=True, index=False, sep='\t')