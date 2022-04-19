import ast
import numpy as np
import pandas as pd


def top_genres(artist):
    genres = pd.Series([x for item in artist['genres'] for x in item]).value_counts().reset_index()[0:10]
    genres.columns = ['feat', 'value']
    genres['feat'] = genres['feat'].str.title()
    genres.index += 1
    return genres

def get_avg_prod_dict(df):
    keys = list(range(0,1440))
    dayInMins = {key: 0 for key in keys}
    prodInMins = {key: 0 for key in keys}
    avgProdInMins = {key: 0 for key in keys}
    for i in range(len(df)):
        productivity = df['productivity_level'][i]
        if df['tempStartMinute'][i] <  df['tempEndMinute'][i]:
            for j in range(df['tempStartMinute'][i], df['tempEndMinute'][i]+1):
                dayInMins[j] += 1
                prodInMins[j] += productivity
                avgProdInMins[j] = prodInMins[j] / dayInMins[j]
        else:
            for j in range(df['tempStartMinute'][i], 1440):
                dayInMins[j] += 1
                prodInMins[j] +=productivity
                avgProdInMins[j] = prodInMins[j] / dayInMins[j]
            for j in range(0, df['tempEndMinute'][i]+1):
                dayInMins[j] += 1
                prodInMins[j] +=productivity
                avgProdInMins[j] = prodInMins[j] / dayInMins[j]
    return avgProdInMins

def bokeh_settings():
    hours = list(range(0,24))
    hours2 = ["{}".format(x) for x in hours]
    hours_in_minutes = np.arange(0, 1440, 60).tolist()
    keys_values = dict(zip(hours_in_minutes, hours2))
    return hours_in_minutes, keys_values