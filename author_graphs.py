"""
script which creates a pyplot graph of 4 graphs (CA CA_AI, LoL, LoL_AI)
"""
import pandas as pd
from itertools import combinations
from collections import Counter
import os
import plotly.graph_objects as go

# From each df, we need to make two dfs : one with total of contributions per countries
# One with all the collaborations between countries

# df with all the countries and the lat, lon of their barycentre
path_country = "data/countries1.csv"
df_country = pd.read_csv(path_country, sep='\t', encoding='utf-8', index_col=False)

for path in os.listdir("data/clean_data"):
    # if path == "CA_full_data_filtered.pkl":
    #     df.CN = df.CN.apply(lambda x: literal_eval(x))
    print(path)
    name = path.split(".")[0]
    df = pd.read_pickle("data/clean_data/" + path)
    df_c = df_country
    edge_list = []
    tot = Counter()
    tot_edge = Counter()

    for index, lst in df.CN.items():
        for country in lst:
            tot[country] += 1
        for pair in combinations(lst, 2):
            if len(set(pair)) > 1:
                res = tuple(sorted(list(pair)))
                tot_edge[res] += 1
    df_c['total'] = df_c['name'].apply(lambda x: tot[x])
    df_c['percentage'] = round(df_c.total * 100 / sum(tot.values()), 1)
    max_art = tot.most_common(1)[0][1]

    df_edge = pd.DataFrame.from_dict(tot_edge, orient="index").reset_index()
    df_edge = df_edge.rename(columns={'index': 'edge', 0: 'total_edge'})
    df_edge["c1"] = df_edge.edge.apply(lambda x: x[0])
    df_edge["c2"] = df_edge.edge.apply(lambda x: x[1])
    df_edge = df_edge.merge(df_country[["latitude", "longitude"]], how="left", left_on=df_edge.c1,
                            right_on=df_country.name)
    df_edge = df_edge.rename(columns={'latitude': 'latitude_c1', 'longitude': 'longitude_c1'})
    df_edge = df_edge.drop(columns="key_0")
    df_edge = df_edge.merge(df_country[["latitude", "longitude"]], how="left", left_on=df_edge.c2,
                            right_on=df_country.name)
    df_edge = df_edge.rename(columns={'latitude': 'latitude_c2', 'longitude': 'longitude_c2'})
    df_edge = df_edge.drop(columns="key_0")
    total_edges = df_edge["total_edge"].sum()

    # Saving the df_c and df_edge
    df_c.to_pickle("data/countries_edges/df_country_"+name)
    df_edge.to_pickle("data/countries_edges/df_edge_"+name)

    # Plotting
    fig = go.Figure()

    for i in range(len(df_country)):
        fig.add_trace(
            go.Scattergeo(
                locationmode="country names",
                text=df_c.percentage,
                lon=df_c.longitude,
                lat=df_c.latitude,
                marker=dict(
                    size=(df_c.total / max_art) * 100,
                    line_width=0,
                    color="blue"
                )
            )
        )

    for i in range(len(df_edge)):
        fig.add_trace(
            go.Scattergeo(
                locationmode='country names',
                lon=[df_edge.longitude_c1[i], df_edge.longitude_c2[i]],
                lat=[df_edge.latitude_c1[i], df_edge.latitude_c2[i]],
                mode="lines",
                line=dict(width=5, color='red'),
                opacity=df_edge["total_edge"][i] / float(df_edge["total_edge"].max())
            )
        )
    fig.update_layout(
        title_text=name + " : Country analysis",
        showlegend=False,
        geo=go.layout.Geo(
            scope="world",
            projection_type="natural earth",
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            showcountries=True,
        ),
        height=1080,
        width=1980

    )
    fig.write_image("/home/kevin-main/PycharmProjects/projet_transdisciplinaire/img/authors_network_map/" + name +
                    ".jpeg")
