# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
sites = list(spacex_df["Launch Site"].unique())
site_list = [{"label": site, "value": site} for site in sites]
site_options = [{"label": "All Sites", "value": "ALL"}]
site_options.extend(site_list)


# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40}
        ),
        # TASK 1: Dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=site_options,
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),

        # TASK 2: Pie chart to show the total successful launches count for
        # all sites
        # If a specific launch site was selected, show the Success vs. Failed
        # counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
        ),

        # TASK 4: Scatter chart to show correlation between payload and
        # launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input,
# `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Launch Sites",
        )
    else:
        # return the outcomes piechart for a selected site
        site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        land_df = site_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(
            land_df,
            values="count",
            names="class",
            title="Landing Types"
        )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs,
# `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure"
    ),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ]
)
def success_pie_chart(entered_site, payload_range):
    plot_df = spacex_df
    mass_col = "Payload Mass (kg)"
    title = "Correlation between payload and success"
    if entered_site != "ALL":
        plot_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        title = f"{title} at {entered_site}"
    rows = np.logical_and(
        plot_df[mass_col] >= payload_range[0],
        plot_df[mass_col] <= payload_range[1],
    )
    plot_df = plot_df[rows]
    fig = px.scatter(
        plot_df,
        x=mass_col,
        y="class",
        color="Booster Version Category",
        title=title,
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server()
