import os
import numpy as np
import streamlit as st

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

# Add all your application here
app.add_page("Spotify Overview", spotify_overview.app)
app.add_page("Audio Features", audio_features_overview.app)
app.add_page("Submit Activity", submit_activity.app)
app.add_page("Activity Overview", activity_overview.app)
app.add_page("Productivity Summary", productivity_summary.app)

# The main app
app.run()