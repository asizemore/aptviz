## Visualization functions
# General packages
import numpy as np
import sys
import pandas as pd

# Plotly
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ApTViz
from aptviz import aptviz_themes
from aptviz.supporting import *

# Load ApTViz visualization theme
pio.templates.default = "aptviz"

# Construct a histogram of prop split/colored by dimension
def fsc_histogram_by_dim(fsc_df, prop = "weight"):
    fig = px.histogram(fsc_df,x=prop, color="dim", marginal="violin", opacity=0.8)
    fig.update_layout(barmode='overlay')
    fig.update_layout(title= f'Distribution of simplex {prop} by dimension')
    return fig

# Construct a histogram of prop using simplices passing a threshold
def fsc_histogram_thresholded(fsc_df, prop = "dim", filter_on = "weight", threshold = 0, keep = "geq"):
    
    if keep == "geq":
        fsc_filtered = fsc_df.loc[fsc_df[filter_on] >= threshold]
    elif keep == "leq":
        fsc_filtered = fsc_df.loc[fsc_df[filter_on] <= threshold]
    else:
        print("Please enter a valid keep value: geq or leq.")
    
    fig = px.histogram(fsc_filtered, x = prop, color_discrete_sequence=["teal"])
    return fig

# Create heatmap of simplex count across the filtration, separated by dimension

def fsc_attribute_across_filtration(fsc_df, filtration_steps, filtration_col="weight"):

    # Calculate max dim from simplicial complex
    max_dim = np.max(fsc_df.dim)
    
    # Need an array of the appropriate size.
    count_across_filtration = np.zeros((filtration_steps.shape[0],(max_dim+1)))

    # Loop across the array and fill the count for each
    for i,filtration_step in enumerate(filtration_steps) :

        if (filtration_col == "weight"):
            thresholded_fsc_temp = fsc_df.loc[fsc_df[filtration_col] >= filtration_step]
        elif (filtration_col == "rank"):
            thresholded_fsc_temp = fsc_df.loc[fsc_df[filtration_col] <= filtration_step]
        else:
            print("Please provide a valid threhsold column (weight or rank)")
        

        count_df_temp = thresholded_fsc_temp.dim.value_counts().to_frame()
       
        count_across_filtration[i, count_df_temp.index.to_numpy()] = count_df_temp.dim.to_numpy(copy=True)[count_df_temp.index.to_numpy()]



    fig = px.imshow(np.transpose(count_across_filtration),
                     height=600,
                     aspect="auto",
                     labels=dict(x="Filtration step", y="Dimension", color="Count simplices"))
    
    return fig


