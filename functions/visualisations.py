import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def polar_plot(df, pad, title, position):
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, projection="polar")
    theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
    # values has the 5 values from 'Col B', with the first element repeated
    values = df['value'].values
    values = np.append(values, values[0])
    # draw the polygon and the mark the points for each angle/value combination
    l1, = ax.plot(theta, values, color="C2", marker="o", label="Name of Col B")
    plt.xticks(theta[:-1], df['feat'], color='grey', size=12)
    #ax.set_xticks(theta[:-1], df['feat'])
    ax.tick_params(pad=pad) # to increase the distance of the labels to the plot
    # fill the area of the polygon with green and some transparency
    ax.fill(theta, values, 'green', alpha=0.1)
    ax.set_yticklabels([])
    # plt.legend() # shows the legend, using the label of the line plot (useful when there is more than 1 polygon)
    plt.title(title)
    position.pyplot(fig)