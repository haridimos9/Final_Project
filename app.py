import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
# Custom imports 
from multipage import MultiPage
from pages import submit_activity, spotify_overview, audio_features_overview, activity_overview, productivity_summary


# Wide page
st.set_page_config(layout="wide") 

# Create an instance of the app 
app = MultiPage()

# Title of the main page
t1, t2 = st.columns((0.07,0.65))  
t1.image('images/Spotify-logo.png', width = 150)
t2.title("Productivity and Spotify")

# Information about the app
with st.expander("ℹ️ - About this app", expanded=True):
    st.write(
    """     
    The Productivity and Spotify is an app which connects your music with your activities to give an overview of your productivity.
    - Spotify Overview: See your favourite artists, songs and genres in three different periods.
    - Audio Features: Interesting metrics based on the music you hear. Every song has its own features which are calculated by Spotify.
    - Submit Activity: Submit your activity and let the app do the job for you. By submitting, you will be able to extract many insights about your productivity based on the music you listen. On the same page you also have the option to delete activities where you made a mistake.
    - Activity Overview: See what kind of music you listen during every activity.
    """
)

# Add all your application here
app.add_page("Spotify Overview", spotify_overview.app)
app.add_page("Audio Features", audio_features_overview.app)
app.add_page("Submit Activity", submit_activity.app)
app.add_page("Activity Overview", activity_overview.app)
app.add_page("Productivity Summary", productivity_summary.app)

# The main app
app.run()
