import pandas as pd


def load_artist(period):
    # Loading data
    artist_one_year = pd.read_csv('data/user_top_artists_data_long_term.csv')
    artist_six_months = pd.read_csv('data/user_top_artists_data_medium_term.csv')
    artist_one_month = pd.read_csv('data/user_top_artists_data_short_term.csv')
    # Map period with data
    if period == 'Last year':
        artist = artist_one_year
    elif period == 'Last six months':
        artist = artist_six_months
    else:
        artist = artist_one_month
    return artist

def load_tracks(period):
    # Loading data
    tracks_one_year = pd.read_csv('data/user_top_tracks_data_long_term.csv')
    tracks_six_months = pd.read_csv('data/user_top_tracks_data_medium_term.csv')
    tracks_one_month = pd.read_csv('data/user_top_tracks_data_short_term.csv')
    # Map period with data
    if period == 'Last year':
        tracks = tracks_one_year
    elif period == 'Last six months':
        tracks = tracks_six_months
    else:
        tracks = tracks_one_month
    return tracks

def load_streaming_history(activity):
    # Loading data
    streaming_history = pd.read_csv('data/StreamingHistory.csv')
    # Map activity with data
    if activity == 'Exercise':
        stream = streaming_history[streaming_history['activity_type']=='exercise'].reset_index(drop=True)
    elif activity == 'Relax':
        stream = streaming_history[streaming_history['activity_type']=='relax'].reset_index(drop=True)
    elif activity == 'Study':
        stream = streaming_history[streaming_history['activity_type']=='study'].reset_index(drop=True)
    else:
        stream = streaming_history[streaming_history['activity_type']=='work'].reset_index(drop=True)
    return stream