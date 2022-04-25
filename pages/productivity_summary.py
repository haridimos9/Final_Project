import numpy as np
import pandas as pd
import streamlit as st
import datetime
from sklearn.preprocessing import MinMaxScaler
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import  ColumnDataSource, Title, HoverTool

from functions.load_data import *
from functions.preprocessing import *
from functions.visualisations import *


def app():

    # Loading data
    data = pd.read_csv('data/saved_data/submission.csv')
    df = pd.read_csv('data/StreamingHistory.csv')

    # Select activity
    option = st.selectbox('Select activity',('Study', 'Relax', 'Exercise', 'Work'))

    # Select dates
    cols = st.columns(2)
    default_start_date = datetime.date(datetime.date.today().year, 1, 1)
    starting_date = cols[0].date_input("Starting Date:", value = default_start_date)
    ending_date = cols[1].date_input("Ending Date:")

    #start_time = cols[1].time_input("Starting Time:", datetime.time())
    #end_time = cols[1].time_input("Ending Time:", datetime.time())
    #starting_date = datetime.datetime.combine(start_date, start_time)#.isoformat()
    #ending_date = datetime.datetime.combine(end_date, end_time)
    
    # Data preprocessing
    data['tempStartTime'] = pd.to_datetime(data['startTime']).dt.time
    data['tempEndTime'] = pd.to_datetime(data['endTime']).dt.time
    data['tempStartMinute'] = pd.to_datetime(data['startTime']).dt.hour*60 + pd.to_datetime(data['startTime']).dt.minute
    data['tempEndMinute'] = pd.to_datetime(data['endTime']).dt.hour*60 + pd.to_datetime(data['endTime']).dt.minute
    data['difference'] = pd.to_datetime(data['endTime']) - pd.to_datetime(data['startTime'])
    data['startTime'] = pd.to_datetime(data['startTime'])
    data['endTime'] = pd.to_datetime(data['endTime'])

    # Filter data
    #starting_date = np.min(data['startTime']).date()
    #ending_date = np.max(data['endTime']).date()
    data = data[(pd.to_datetime(data['startTime']).dt.date >= starting_date) & (pd.to_datetime(data['endTime']).dt.date <= ending_date)]

    # Filter on activity
    data = data[data['activity_type']==option.lower()].reset_index(drop=True)
    df = load_streaming_history(option)

    # Data preprocessing for df
    df['genres'] = df['genres'].map(lambda x: ast.literal_eval(x)) # string to list format
    pd.Series([x for item in df['genres'] for x in item]).value_counts().reset_index()[0:10]
    df['endTime'] = pd.to_datetime(df['endTime'])
    df["productivity_level"] = np.nan
    for idx in range(len(data)):
        df.loc[(df['endTime']>=data['startTime'][idx]) & (df['endTime']<=data['endTime'][idx]), "productivity_level"] = data.loc[idx,"productivity_level"]
    
    # Create dataframe
    df_avg = get_avg_prod_dict(data)
    df_index = pd.DataFrame({'A' : np.arange(1440)},index=pd.to_timedelta(np.arange(1440),unit='m')).reset_index()
    df_index = df_index['index'].astype(str).map(lambda x: x[7:])
    avg = pd.DataFrame(df_avg.items(), columns=['minute', 'values'])
    avg = avg.merge(df_index.rename('minute_index'), left_index=True, right_index=True)
    avg = avg.set_index('minute')

    # Axis ticks
    hours_in_minutes, keys_values = bokeh_settings()

    st.markdown("<h3 style='text-align: center; color: grey;'>Select a productivity level to see Genres and Audio Features for that productivity level</h3>", unsafe_allow_html=True)

    # Select productivity
    #emojis = ['😡','😞', '😐', '🙂', '😃']
    #colmns = st.columns(3)
    #emoji_rating = colmns[1].select_slider('Select productivity:', options=emojis, value='😐')#, format_func = lambda x: "option " + str(x))
    #rating = emojis.index(emoji_rating) + 1
    #rating = st.slider("Select productivity:", 1, 5, 1)
    col = st.columns(15)
    rating_1 = col[5].button('😡')
    rating_2 = col[6].button('😞')
    rating_3 = col[7].button('😐')
    rating_4 = col[8].button('🙂')
    rating_5 = col[9].button('😃')

    rating = 3

    if rating_1:
        rating = 1
    elif rating_2:
        rating = 2
    elif rating_3:
        rating = 3
    elif rating_4:
        rating = 4
    else:
        rating = 5

    # Filter on productivity
    df = df[df['productivity_level']==rating].reset_index(drop=True)

    if df.empty:
        # Show message
        left, center, right = st.columns(3)
        center.markdown("<h3 style='text-align: center; color: grey;'>No available data</h3>", unsafe_allow_html=True)
    else:
        # Genre column
        df_genre = pd.Series([x for item in df['genres'] for x in item]).value_counts().reset_index()[0:10]
        df_genre.columns = ['feat', 'value']

        # Audio features
        audio_feats_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                            'instrumentalness', 'liveness', 'valence', 'tempo']
        scaler = MinMaxScaler()
        polar_trackfeatures = df[audio_feats_cols]    
        for _col in polar_trackfeatures.columns:
            polar_trackfeatures[f'{_col}'] = [x[0] for x in scaler.fit_transform(pd.DataFrame(polar_trackfeatures[f'{_col}'].values.reshape(-1, 1))).tolist()]
        polar_trackfeatures = polar_trackfeatures.mean().reset_index()
        polar_trackfeatures.columns = ['feat', 'value']

        # Split to three columns
        #left, center, right = st.columns(3)
        
        # Subtitle
        #center.markdown("<h3 style='text-align: center; color: grey;'>Genre and Audio features</h3>", unsafe_allow_html=True)

        # Polar plots
        left, right = st.columns(2)
        polar_plot(df_genre, 20, "", left)
        polar_plot(polar_trackfeatures, 20, "", right)

    # Title
    left, center, right = st.columns(3)
    center.markdown("<h3 style='text-align: center; color: grey;'>Productivity distribution for a specific date interval</h3>", unsafe_allow_html=True)

    # Visualization 1
    src = ColumnDataSource(avg)
    p = figure(plot_width = 600, plot_height = 500, title = 'Average productivity within the 24 hours of the day for every activity',
            x_axis_label = "Hours" , y_axis_label = 'Avg Productivity')
    bar = p.vbar(x='minute', top='values', source = src)
    p.xaxis.ticker = hours_in_minutes
    p.xaxis.major_label_overrides = keys_values
    p.add_tools(HoverTool(renderers=[bar],
                        tooltips = [('Minute', '@minute_index'), 
                                    ('Avg. Productivity', '@values{0.2f}')],
                        mode='mouse'))
    st.bokeh_chart(p, use_container_width=True)

    # Visualization 2
    src = ColumnDataSource(data)
    p = figure(plot_width = 600, plot_height = 500, x_axis_type='datetime', title = 'Productivity by date within the specified datetime frame',
            x_axis_label = "Date" , y_axis_label = 'Productivity') 
    bar = p.vbar(x='startTime', top='productivity_level', source = src, width = 'difference')
    p.add_tools(HoverTool(renderers=[bar],
                        tooltips = [('Start time: ', '@startTime{%F %H:%M}'),
                                    ('End time: ', '@endTime{%F %H:%M}'),
                                    ('Activity:', '@activity_type'),
                                    ('Productivity', '@productivity_level{0.2f}')], 
                        formatters={'@startTime': 'datetime', '@endTime': 'datetime'},
                        mode='mouse'))
    st.bokeh_chart(p, use_container_width=True)#