import ast
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

from functions.load_data import *
from functions.visualisations import *


def app():
    
    # Select period
    option = st.selectbox('Select period',('Last year', 'Last six months', 'Last month'))

    # Loading data
    tracks = load_tracks(option)
    features = pd.read_csv('data/user_tracks_audio_features.csv')

    # Assign now
    temp = tracks[['song_name', 'song_external_url']]

    # Join features with tracks
    temp['track_id'] = temp['song_external_url'].str[31:]
    trackfeatures = pd.merge(temp, features, on='track_id')
    
    # Preprocessing for polar plot
    audio_feats_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo']
    scaler = MinMaxScaler()
    polar_trackfeatures = trackfeatures[audio_feats_cols]
    for _col in polar_trackfeatures.columns:
        polar_trackfeatures[f'{_col}'] = [x[0] for x in scaler.fit_transform(pd.DataFrame(polar_trackfeatures[f'{_col}'].values.reshape(-1, 1))).tolist()]
    polar_trackfeatures = polar_trackfeatures.mean().reset_index()
    polar_trackfeatures.columns = ['feat', 'value']

    # Metrics
    m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
    m1.metric(label ='Mean energy level', value = round(trackfeatures["energy"].mean(),3))
    m2.metric(label ='Mean loudness level', value = round(trackfeatures["loudness"].mean(),3))
    m3.metric(label ='Mean speechiness level', value = round(trackfeatures["speechiness"].mean(),3))
    m4.metric(label ='Mean liveness level', value = round(trackfeatures["liveness"].mean(),3))
    m5.metric(label ='Mean danceability level', value = round(trackfeatures["danceability"].mean(),3))
    m1, m2, m3, m4, m5, m6 = st.columns((1,1,1,1,1,1))
    m2.metric(label ='Mean tempo level', value = round(trackfeatures["tempo"].mean(),3))
    m3.metric(label ='Mean valence level', value = round(trackfeatures["valence"].mean(),3))
    m4.metric(label ='Mean instrumentalness level', value = round(trackfeatures["instrumentalness"].mean(),3))
    m5.metric(label ='Mean acousticness level', value = round(trackfeatures["acousticness"].mean(),3))

    # Top 5 for every feature
    energy = trackfeatures.sort_values(by='energy', ascending=False).reset_index(drop=True)[['song_name', 'energy']][0:5]
    energy.index += 1
    energy.columns = ['Track Name', 'Energy']
    loudness = trackfeatures.sort_values(by='loudness', ascending=False).reset_index(drop=True)[['song_name', 'loudness']][0:5]
    loudness.index += 1
    loudness.columns = ['Track Name', 'Loudness']
    speechiness = trackfeatures.sort_values(by='speechiness', ascending=False).reset_index(drop=True)[['song_name', 'speechiness']][0:5]
    speechiness.index += 1
    speechiness.columns = ['Track Name', 'Speechiness']
    liveness = trackfeatures.sort_values(by='liveness', ascending=False).reset_index(drop=True)[['song_name', 'liveness']][0:5]
    liveness.index += 1
    liveness.columns = ['Track Name', 'Liveness']
    danceability = trackfeatures.sort_values(by='danceability', ascending=False).reset_index(drop=True)[['song_name', 'danceability']][0:5]
    danceability.index += 1
    danceability.columns = ['Track Name', 'Danceability']
    tempo = trackfeatures.sort_values(by='tempo', ascending=False).reset_index(drop=True)[['song_name', 'danceability']][0:5]
    tempo.index += 1
    tempo.columns = ['Track Name', 'Tempo']
    valence = trackfeatures.sort_values(by='valence', ascending=False).reset_index(drop=True)[['song_name', 'danceability']][0:5]
    valence.index += 1
    valence.columns = ['Track Name', 'Valence']
    instrumentalness = trackfeatures.sort_values(by='instrumentalness', ascending=False).reset_index(drop=True)[['song_name', 'danceability']][0:5]
    instrumentalness.index += 1
    instrumentalness.columns = ['Track Name', 'Instrumentalness']
    acousticness = trackfeatures.sort_values(by='acousticness', ascending=False).reset_index(drop=True)[['song_name', 'danceability']][0:5]
    acousticness.index += 1
    acousticness.columns = ['Track Name', 'Acousticness']

    # Split to three columns
    left, center, right = st.columns(3)

    # Subtitle
    center.markdown("<h3 style='text-align: center; color: grey;'>Top 5 tracks for audio features</h3>", unsafe_allow_html=True)

    # Split to three columns
    left, center, right = st.columns(3)

    # Three tables
    left.dataframe(energy)
    center.dataframe(loudness)
    right.dataframe(speechiness)

    # Split to five columns
    _, left, _, right, _ = st.columns(5)

    # Two tables
    left.dataframe(liveness)
    right.dataframe(danceability)

    # Split to three columns
    left, center, right = st.columns(3)
    polar_plot(polar_trackfeatures, 20, "Audio features overview", center)

    # Split to four columns
    _, left, right, _ = st.columns(4)

    # Two tables
    left.dataframe(tempo)
    right.dataframe(valence)

    # Split to four columns
    left, _, _, right = st.columns(4)

    # Two tables
    left.dataframe(instrumentalness)
    right.dataframe(acousticness)