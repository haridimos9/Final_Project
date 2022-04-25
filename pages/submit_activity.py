import csv
import os.path
import datetime
import numpy as np
import pandas as pd
import streamlit as st


def app():

    form_1 = st.form(key="Submit")
    if os.path.exists("./data/saved_data/submission.csv"):
        form_2 = st.form(key="Delete")

    with form_1:
        cols = st.columns((1, 1))
        activity = st.selectbox(
            "Report activity:", ["Exercise", "Relax", "Study", "Work"], index=2
        )
        activity = activity.lower()
        #comment = st.text_area("Comment:")
        cols = st.columns(2)
        start_date = cols[0].date_input("Starting Date:", datetime.date.today())
        start_time = cols[1].time_input("Starting Time:", datetime.datetime.now())
        end_date = cols[0].date_input("Ending Date:", datetime.date.today() + datetime.timedelta(days=1))
        end_time = cols[1].time_input("Ending Time:", datetime.datetime.now() + datetime.timedelta(hours=1))        
        start_datetime = datetime.datetime.combine(start_date, start_time)#.isoformat()
        end_datetime = datetime.datetime.combine(end_date, end_time)#.isoformat()

        col = st.columns(15)
        rating_1 = col[5].form_submit_button('😡')
        rating_2 = col[6].form_submit_button('😞')
        rating_3 = col[7].form_submit_button('😐')
        rating_4 = col[8].form_submit_button('🙂')
        rating_5 = col[9].form_submit_button('😃')

        submitted = st.form_submit_button(label="Submit", help='When pressed the form is submitted with the information that you have inserted. Once submitted the results will be combined with the music that you listened at that time to discover interesting trends between your productivity and your music habits.')
            
    if rating_1:
        with open("./data/saved_data/rating.txt", "w") as output:
            output.write(str(1))
    if rating_2:
        with open("./data/saved_data/rating.txt", "w") as output:
            output.write(str(2))
    if rating_3:
        with open("./data/saved_data/rating.txt", "w") as output:
            output.write(str(3))
    if rating_4:
        with open("./data/saved_data/rating.txt", "w") as output:
            output.write(str(4))
    if rating_5:
        with open("./data/saved_data/rating.txt", "w") as output:
            output.write(str(5))

    if os.path.exists("./data/saved_data/submission.csv"):
        with form_2:
            cols = st.columns((1, 1))
            form = pd.read_csv('./data/saved_data/submission.csv')
            row = st.number_input('Select the index of the row that you wish to be deleted', min_value=1, max_value=np.max(form.index), format='%i')
            deleted = st.form_submit_button(label="Delete", help="Once pressed, it will the inserted value with the respective index. It's scope is to be used to correct wrong inputs.")

    if submitted:
        with open('./data/saved_data/rating.txt') as f:
            rating = int(f.readlines()[0])
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
        if deleted:
            form = pd.read_csv('./data/saved_data/submission.csv')
            form = form.sort_values(by=['startTime'], ascending=False).reset_index(drop=True)
            form.index += 1
            form = form.drop(row).reset_index(drop=True)
            form.to_csv('./data/saved_data/submission.csv', index=False)
            st.success("Your rating was deleted.")

    if os.path.exists("./data/saved_data/submission.csv"):
        expander = st.expander("See all records")
        with expander:
            submit_form = pd.read_csv('./data/saved_data/submission.csv')
            submit_form = submit_form.sort_values(by=['startTime'], ascending=False).reset_index(drop=True)
            submit_form.index += 1
            st.dataframe(submit_form, 2000, 1000)
