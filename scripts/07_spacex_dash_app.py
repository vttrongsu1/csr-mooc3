"""
SpaceX Launch Records Interactive Dashboard using Plotly Dash
IBM Data Science Professional Certificate - Capstone Project
"""

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX launch data
spacex_df = pd.read_csv("data/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash application
app = dash.Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

# Create application layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#0B1E36', 'font-size': 36, 'marginBottom': 20}
    ),
    
    # TASK 1: Add a Launch Site Dropdown Input Component
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True,
        style={'width': '80%', 'margin': '0 auto', 'padding': '3px', 'fontSize': '18px'}
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site is selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart'), style={'width': '85%', 'margin': '0 auto'}),
    html.Br(),

    html.P("Payload range (Kg):", style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': 18}),
    
    # TASK 3: Add a slider to select payload range
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={0: '0 kg', 2500: '2,500 kg', 5000: '5,000 kg', 7500: '7,500 kg', 10000: '10,000 kg'},
            value=[min_payload, max_payload]
        )
    ], style={'width': '80%', 'margin': '0 auto'}),
    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'), style={'width': '85%', 'margin': '0 auto'})
])


# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by All Sites',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = filtered_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['label'] = outcome_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome_counts,
            values='count',
            names='label',
            title=f'Landing Outcome Distribution for Site: {entered_site}',
            color='label',
            color_discrete_map={'Success': '#10B981', 'Failure': '#EF4444'}
        )
        return fig


# TASK 4: Add a callback function to render success-payload-scatter-chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload Mass and Success for All Sites',
            hover_data=['Flight Number', 'Launch Site', 'Booster Version']
        )
        fig.update_layout(yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Failure (0)', 'Success (1)']))
        return fig
    else:
        filtered_df_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df_site,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation Between Payload Mass and Success for Site: {entered_site}',
            hover_data=['Flight Number', 'Booster Version']
        )
        fig.update_layout(yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Failure (0)', 'Success (1)']))
        return fig


# Run application
if __name__ == '__main__':
    print("Starting Dash server on http://127.0.0.1:8050 ...")
    app.run(debug=False, port=8050)
