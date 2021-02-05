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
from aptviz.aptviz_themes import *

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
    
    fig = px.histogram(fsc_filtered, x = prop, color_discrete_sequence=["#995949"])
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


# Create paired violin plot comparing distribution of simplices split by dimension
def fsc_violin_compare_by_dim(fsc_df, indicator_col, prop = "weight"):

    fig = go.Figure()

    # Calculate max dim from simplicial complex
    max_dim = np.max(fsc_df.dim.astype(int))

    for dim in np.arange(max_dim+1):

        # Subset the dataframe by current dimension
        temp_df = fsc_df[fsc_df["dim"] == dim]

        # Add indicator column violin
        fig.add_trace(go.Violin(x=temp_df["dim"][temp_df[indicator_col] == 1],
                                y=temp_df[prop][temp_df[indicator_col] == 1],
                                legendgroup = "Yes",
                                scalegroup="Yes",
                                name = f'{indicator_col} dim {dim}',
                                side = "negative",
                                line_color = davos_colors[dim],
                                pointpos = -1.3))

        # Add entire complex violin
        fig.add_trace(go.Violin(x=temp_df["dim"],
                                y=temp_df[prop],
                                legendgroup = "Yes",
                                scalegroup="No",
                                name = f'All dim {dim}',
                                side = "positive",
                                line_color = davos_colors[dim],
                                pointpos = 1.3,
                                opacity = 0.5))

    fig.update_traces(meanline_visible=True,
                      points='all', # show all points
                      marker_size = 3,
                      marker_opacity = 0.6,
                      jitter = 0.2,
                      scalemode='width') # or "count"
    fig.update_layout(violingap=0,
                      violinmode='overlay',
                      violingroupgap = 0.5)

    fig.update_xaxes(
        title_text="dim"
    )
    fig.update_yaxes(
        title_text=prop
    )
    
    return fig


# Plot overlaid persistence diagram
def plot_pd(bar_df, axis_range):

    # Calculate maximum dimension
    max_dim = np.max(bar_df["bar_dim"].astype(int))

    fig = px.scatter(bar_df, x="bar_birth", y="bar_death", color="bar_dim",
                     title="Persistence Diagrams (overlayed)", hover_data = ["rep"],
                     category_orders = {"bar_dim":[str(x) for x in np.arange(max_dim)]})



    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
        range = axis_range,
        title_text="death",
        zeroline = False
      )

    fig.update_xaxes(
        range = axis_range,
        constrain='domain',
        title_text="birth",
        layer = "above traces",
        zeroline = False
    )

    fig.update_traces(mode='markers',
                      marker_opacity=0.7,
                      marker_size=12,
                      marker_line_color = my_charcoal,
                      marker_line_width = 0.2)
    
    fig.update_layout(hovermode = 'closest')

    fig.add_trace(
        go.Scatter(
            x=axis_range,
            y=axis_range,
            mode="lines",
            line=go.scatter.Line(color= 'rgba(187, 190, 191, .9)', width=0.5),
            showlegend=False,
            opacity = 0.6)
    )

    
    return fig

