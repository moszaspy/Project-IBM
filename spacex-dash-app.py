
# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get minimum and maximum payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# =====================================================
# APP LAYOUT
# =====================================================

app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Add Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add Pie Chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # TASK 3: Add Range Slider
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add Scatter Chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])


# =====================================================
# TASK 2: PIE CHART CALLBACK
# =====================================================

@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)

def get_pie_chart(entered_site):

    filtered_df = spacex_df

    if entered_site == 'ALL':

        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Launch Site'
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failed Launches for {entered_site}'
        )

        return fig


# =====================================================
# TASK 4: SCATTER PLOT CALLBACK
# =====================================================

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)

def get_scatter_chart(entered_site, entered_payload):

    filtered_df = spacex_df

    if entered_site == 'ALL':

        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= entered_payload[0]) &
            (spacex_df['Payload Mass (kg)'] <= entered_payload[1])
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload Mass vs. Launch Outcome for All Sites'
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        filtered_df = filtered_df[
            (filtered_df['Payload Mass (kg)'] >= entered_payload[0]) &
            (filtered_df['Payload Mass (kg)'] <= entered_payload[1])
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload Mass vs. Launch Outcome for {entered_site}'
        )

        return fig


# =====================================================
# RUN THE APPLICATION
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)
