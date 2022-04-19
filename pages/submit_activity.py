import csv
import os.path
import datetime
import pandas as pd
import streamlit as st


def app():
    
    form = st.form(key="annotation")

    with form:
        cols = st.columns((1, 1))
        activity = st.selectbox(
            "Report activity:", ["Exercise", "Relax", "Study", "Work"], index=2
        )
        activity = activity.lower()
        #comment = st.text_area("Comment:")
        cols = st.columns(2)
        start_date = cols[0].date_input("Starting Date:")
        start_time = cols[1].time_input("Starting Time:", datetime.time())
        end_date = cols[0].date_input("Ending Date:")
        end_time = cols[1].time_input("Ending Time:", datetime.time())
        start_datetime = datetime.datetime.combine(start_date, start_time)#.isoformat()
        end_datetime = datetime.datetime.combine(end_date, end_time)#.isoformat()
        
        #rating = st.slider("Rate productivity:", 1, 5, 1)
        emojis = ['😡','😞', '😐', '🙂', '😃']
        colmns = st.columns(3)
        emoji_rating = colmns[1].select_slider('Select productivity:', options=emojis)#, format_func = lambda x: "option " + str(x))
        rating = emojis.index(emoji_rating) + 1
        #colmns = st.columns(3)
        #rating = colmns[1].select_slider('Rate productivity:', options=['😡','😞', '😐', '🙂', '😃'])
        #rating = st.checkbox('I agree')
        submitted = st.form_submit_button(label="Submit")

    if submitted:
        if start_datetime > end_datetime:
            st.error('Starting time is after ending time')
        else:
            if os.path.exists("./data/saved_data/submission.csv"):
                with open('./data/saved_data/submission.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([activity, start_datetime, end_datetime, rating])
            else:
                with open('./data/saved_data/submission.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["activity_type", "startTime", "endTime", "productivity_level"])
                    writer.writerow([activity, start_datetime, end_datetime, rating])
            st.success("Your rating was recorded.")
            st.balloons()

    if os.path.exists("./data/saved_data/submission.csv"):
        expander = st.expander("See all records")
        with expander:
            submit_form = pd.read_csv('./data/saved_data/submission.csv')
            submit_form.index += 1
            st.dataframe(submit_form, 2000, 1000)
