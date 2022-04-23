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
    center.markdown("<h2 style='text-align: center; color: grey;'>Top 5 tracks for every different audio feature</h2>", unsafe_allow_html=True)

    # Split to three columns
    left, center, right = st.columns(3)

    # Three tables
    left.table(energy)
    center.table(loudness)
    right.table(speechiness)

    # Split to five columns
    _, left, _, right, _ = st.columns(5)

    # Two tables
    left.table(liveness)
    right.table(danceability)

    # Split to three columns
    left, center, right = st.columns(3)
    polar_plot(polar_trackfeatures, 20, "Audio features overview", center)

    # Split to four columns
    _, left, right, _ = st.columns(4)

    # Two tables
    left.table(tempo)
    right.table(valence)

    # Split to four columns
    left, _, _, right = st.columns(4)

    # Two tables
    left.table(instrumentalness)
    right.table(acousticness)

    # Explain every measure
    st.info(
    """
    - Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
    - Danceability: Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
    - Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.
    - Instrumentalness: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal.” The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
    - Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
    - Speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
    - Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
    - Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
    """
    )