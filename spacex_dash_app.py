# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sitelist = [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()]
sitelist.insert(0,{'label': 'ALL', 'value': 'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([
                                dcc.Dropdown(id='site-dropdown', 
                                # Update dropdown values using list comphrehension
                                options=sitelist,
                                placeholder="Select a Launch Site",
                                value='ALL',
                                style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 
                                'center'},
                                searchable=True
                                )
                                # Place them next to each other using the division style
                                ], style={'display': 'flex'}), 
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                min=0,max=10000,step=1000,
                                value=[min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_piechart(selected_site):

    # check site selection
    if selected_site == "ALL":
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success/Failure of Launches for {0}'.format(selected_site))       
    else:
        filtered_data = spacex_df[spacex_df['Launch Site']==selected_site]
        fig = px.pie(filtered_data, names='class', title='Success/Failure of Launches for {0}'.format(selected_site))       

    # Pie chart for the sucess and failures
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
def get_scatterchart(selected_site, payload_range):

    low, high = payload_range
    filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]

    # filter on selected site
    if selected_site != "ALL":
        filtered_data = filtered_data[filtered_data['Launch Site']==selected_site]

    # Scatter chart for the sucess and failures
    fig = px.scatter(filtered_data, x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for {0} site(s)'.format(selected_site) )    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
