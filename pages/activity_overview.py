import ast
import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

from functions.load_data import *
from functions.visualisations import *


def app():
    
    # Loading data
    submission = pd.read_csv('data/saved_data/submission.csv')

    # Polar submission
    temp_submission =  pd.DataFrame(submission['activity_type'].value_counts()).reset_index()
    temp_submission.columns = ['feat', 'value']
    
    # Polar plot
    left, center, right = st.columns(3)
    polar_plot(temp_submission, 20, "When do you listen to music?", center)
    
    # Select activity
    option = st.selectbox('Select activity',('Exercise', 'Relax', 'Study', 'Work'))

    # Loading data
    stream = load_streaming_history(option)

    # Genre column
    stream['genres'] = stream['genres'].map(lambda x: ast.literal_eval(x)) # string to list format
    df_genre = pd.Series([x for item in stream['genres'] for x in item]).value_counts().reset_index()[0:10]
    df_genre.columns = ['feat', 'value']
    genre_title = "What genre do you like when you " + option.lower() 

    # Audio features
    audio_feats_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo']
    scaler = MinMaxScaler()
    polar_trackfeatures = stream[audio_feats_cols]    
    for _col in polar_trackfeatures.columns:
        polar_trackfeatures[f'{_col}'] = [x[0] for x in scaler.fit_transform(pd.DataFrame(polar_trackfeatures[f'{_col}'].values.reshape(-1, 1))).tolist()]
    polar_trackfeatures = polar_trackfeatures.mean().reset_index()
    polar_trackfeatures.columns = ['feat', 'value']

    # Split to three columns
    left, center, right = st.columns(3)
    
    # Subtitle
    center.markdown("<h3 style='text-align: center; color: grey;'>Genre and Audio features</h3>", unsafe_allow_html=True)

    # Polar plots
    left, right = st.columns(2)
    polar_plot(df_genre, 20, "", left)
    polar_plot(polar_trackfeatures, 20, "", right)

    # Song popularity table
    track_popularity = stream['track_name'].value_counts().reset_index()[0:10]
    track_popularity.index += 1
    track_popularity.columns = ['Track name', 'Count']
    track_popularity['Count'] = track_popularity['Count']

    # Artist popularity table
    artist_popularity = stream['track_artist'].value_counts().reset_index()[0:10]
    artist_popularity.index += 1
    artist_popularity.columns = ['Artist', 'Count']
    artist_popularity['Count'] = artist_popularity['Count']
    
    # Split to two columns
    left, right = st.columns(2)

    # Most listened song
    left.markdown("<h3 style='text-align: center; color: grey;'>Most listened tracks</h3>", unsafe_allow_html=True)
    left.dataframe(track_popularity)
    
    # Most listened artist
    right.markdown("<h3 style='text-align: center; color: grey;'>Most listened artists</h3>", unsafe_allow_html=True)
    right.dataframe(artist_popularity)