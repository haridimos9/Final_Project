import ast
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from functions.load_data import *
from functions.preprocessing import *
from functions.visualisations import *


def app():
    
    # Select period
    option = st.selectbox('Select period',('Last year', 'Last six months', 'Last month'))

    # Loading data
    artist = load_artist(option)
    tracks = load_tracks(option)

    # Assign now
    artist_popularity = artist.sort_values(by='popularity', ascending=False).reset_index(drop=True)[['name', 'popularity']][0:10]
    track_popularity = tracks.sort_values(by='song_popularity', ascending=False).reset_index(drop=True)[['song_name', 'song_popularity']][0:10]

    # Preprocess artists
    artist['followers'] = artist['followers'].astype(int) # followers to int
    artist['genres'] = artist['genres'].map(lambda x: ast.literal_eval(x)) # string to list format
    genres = top_genres(artist) # load genres
    artist['genres'] = artist['genres'].map(lambda x: x[0] if x!=[] else '').str.title() # keep first genre
    artist = artist[['name', 'popularity', 'followers', 'genres']][0:20] # show only 20 values
    artist.index += 1 # start index from 1
    artist.columns = ['Artist', 'Popularity', 'Followers', 'Genre'] # change column names
    artist['Popularity'] = artist['Popularity'].astype(int)

    # Preprocess tracks
    tracks = tracks[['song_name','artist_name','song_popularity','song_duration']][0:20]
    tracks.index += 1
    tracks.columns = ['Track name', 'Artist', 'Popularity', 'Duration']
    tracks['Popularity'] = tracks['Popularity'].astype(int)

    # Split to two columns
    left, right = st.columns(2)

    # Artist table
    left.markdown("<h3 style='text-align: center; color: grey;'>Top 20 artists</h3>", unsafe_allow_html=True)
    left.dataframe(artist, 2000, 1000)

    # Song table
    right.markdown("<h3 style='text-align: center; color: grey;'>Top 20 songs</h3>", unsafe_allow_html=True)
    right.dataframe(tracks, 2000, 1000)

    # Song popularity table
    track_popularity.index += 1
    track_popularity.columns = ['Track name', 'Popularity']
    track_popularity['Popularity'] = track_popularity['Popularity'].astype(int)

    # Artist popularity table
    artist_popularity.index += 1
    artist_popularity.columns = ['Artist', 'Popularity']
    artist_popularity['Popularity'] = artist_popularity['Popularity'].astype(int)

    # Genre popularity table
    genre_popularity = genres.copy()
    genre_popularity.columns = ['Genre', 'Count']

    # Top artist popularity
    artist_polar = artist[['Artist', 'Popularity']][0:10]
    artist_polar.columns = ['feat', 'value']

    # Split to two columns
    left, right = st.columns(2)

    # Polar plots
    polar_plot(artist_polar, 20, "Popularity on your top artists", left)
    polar_plot(genres, 20, "What do you listen to (generally)?", right)

    # Split to three columns
    left, center, right = st.columns(3)

    # Genre table
    center.markdown("<h3 style='text-align: center; color: grey;'>Top 10 genres</h3>", unsafe_allow_html=True)
    center.dataframe(genre_popularity)

    # Most popular song
    left.markdown("<h3 style='text-align: center; color: grey;'>Top 10 popular songs</h3>", unsafe_allow_html=True)
    left.dataframe(track_popularity)
    
    # Most popular artist
    right.markdown("<h3 style='text-align: center; color: grey;'>Top 10 popular artists</h3>", unsafe_allow_html=True)
    right.dataframe(artist_popularity)