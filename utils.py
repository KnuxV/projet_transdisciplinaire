"""
Functions
"""
import numpy as np
import pandas as pd
import re


def trim_py(df, start_year, end_year, inclusive="both"):
    """

    Parameters
    ----------
    df : dataframe
        the dataframe in which we need to restict the year (PY columns)
    start_year : int
    end_year : int
    inclusive : str
        Either both, left, right or neither

    Returns
    -------
    def_new
        a datagrame where the PY column is restricted between the two dates

    """
    df_new = df
    df_new.PY = df_new.PY.fillna(0)
    df_new.PY = pd.to_numeric(df_new.PY, downcast="integer", errors="coerce")

    condition_year = df_new.PY.between(start_year, end_year, inclusive=inclusive)
    def_new = df_new[condition_year]
    return def_new


def country_name_fixing(df):
    """

    Parameters
    ----------
    df

    Returns
    -------
    def_new
        Where the CN (country) column is created based on the C1 (=adress column), it the a list of the countries of
        all the authors.
        Country names respect the proper terminology to be displayed by plotly. Therefore modification must be made.
    """
    df_country = pd.read_csv("data/countries1.csv", encoding="utf-8", sep="\t")
    def_new = df
    # Given the C1 structure, we extract the last group of words of each address.
    # Two possibilities [Names] Address ; [Names] Address or if no Names just the address.
    reg = re.compile(r"(\[([^\[\]]+)])? (?P<country>[^\[\];]+);?")
    # To respect plotly country names
    dic_country = {'Peoples R China': "China", 'England': 'United Kingdom', 'Scotland': 'United Kingdom',
                   'Wales': 'United Kingdom', 'Northen Ireland': 'United Kingdom'}

    def_new["CN"] = def_new.C1.apply(
        lambda x: [match.group("country").split(", ")[-1] for match in re.finditer(reg, x)] if type(
            x) == str else np.NaN)
    # We get rid of country name for the US (example :  MA 02139 USA ==> United States)
    def_new.CN = def_new.CN.apply(
        lambda x: [country if "USA" not in country else "United States" for country in x] if type(
            x) == list else np.NaN)
    # countries in the dic_country see their name modified
    def_new.CN = def_new.CN.apply(
        lambda x: [dic_country[country] if country in dic_country else country for country in x] if type(
            x) == list else np.NaN)
    # removing everything that is not a country
    def_new.CN = def_new.CN.apply(lambda x: [country for country in x if country in df_country.name.values])

    return def_new


def save_df(df, path, typ="pickle", header=True, index=False, sep="\t",
            columns=None):
    """

    Parameters
    ----------
    columns
    typ : str
        picke or csv
    df : dataframe
        that needs to be saved
    path : a path
        where to save it

    header : header option from pandas
        don't modify
    index : index option from pandas
        don't modify
    sep : sep option from pandas
        don't modify

    Returns
    -------
    nothing
        save the dataframe as a csv or pickle at the chosen location.
    """
    if columns is None:
        columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY', 'CN']
    if typ == "csv":
        df.to_csv(path, columns=columns, header=header, index=index, sep=sep)
    else:
        df.to_pickle(path)
