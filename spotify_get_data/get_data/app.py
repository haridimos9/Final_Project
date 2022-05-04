import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import ast
import dash_table
from flask import Flask, request, redirect, render_template, url_for, session


css_values = {
    'title_fontSize': '25px',
    'description_fontSize': '16px',
}


def create_user_top_artists_across_periods(df_long_term, df_medium_term, df_short_term, entity="artist"):
    """
    From three csv files create on with the all the artists as the first column and another 3 columns
    corresponding to rank of this artist in the periods 'All Time', 'Last 6 Months', 'Last Month'.
    """
    entity_name = 'name' if entity.lower() == "artist" else "song_name"
    long_term_names = df_long_term[entity_name].tolist()
    medium_term_names = df_medium_term[entity_name].tolist()
    short_term_names = df_short_term[entity_name].tolist()

    for m in medium_term_names:
        if m not in long_term_names:
            long_term_names.append(m)
    for s in short_term_names:
        if s not in long_term_names:
            long_term_names.append(s)

    long_term_position, medium_term_position, short_term_position = [], [], []
    for t in long_term_names:
        try:
            long_term_position.append(
                df_long_term.loc[df_long_term[entity_name] == t].index.values[
                    0] + 1)
        except IndexError:
            long_term_position.append('-')
        try:
            medium_term_position.append(
                df_medium_term.loc[df_medium_term[entity_name] == t].index.values[
                    0] + 1)
        except IndexError:
            medium_term_position.append('-')
        try:
            short_term_position.append(
                df_short_term.loc[df_short_term[entity_name] == t].index.values[
                    0] + 1)
        except IndexError:
            short_term_position.append('-')

    user_top_artists_across_periods_df = pd.DataFrame()
    user_top_artists_across_periods_df[entity.capitalize()] = long_term_names
    user_top_artists_across_periods_df['All Time'] = long_term_position
    user_top_artists_across_periods_df['Last 6 Months'] = medium_term_position
    user_top_artists_across_periods_df['Last Month'] = short_term_position
    return user_top_artists_across_periods_df



def init_callbacks(dash_app):
    print('Initiated Callback')

    @dash_app.callback(Output('intermediate-get-user-all-tracks-with-audio-features-for-scatter-polar', 'children'),
                       [Input('scatter_polar_energy_track_number', 'value')])
    def intermediate_get_user_all_tracks_with_audio_features_for_scatter_polar(value):
        if __name__ == '__main__':
            users = pd.read_csv('../data/users.csv')
            user_id = users.iloc[-1]['id']
        else:
            user_id = session['user_id']

        return print('something went well... good')

    


def main():
    if __name__ == '__main__':
        users = pd.read_csv('../data/users.csv')
        user_id = users.iloc[-1]['id']
    else:
        user_id = session['user_id']
    print(f'+++ User {user_id} just accessed the app.')

    #read data
    user_top_artists_data_long_term = pd.read_csv(f'../data/{user_id}/user_top_artists_data_long_term.csv')
    


