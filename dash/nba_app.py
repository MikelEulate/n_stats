## Dashboard to predict nba games:

import dash
import dash_table
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import style
#from tqdm import tqdm
import requests
import time
import json
import datetime

import sys
sys.path.insert(0, '/home/mikel/mikel_wind/nba_prediction/executables')

import get_nba_data as NBA
import NBAFunctions as NBAF


file_name = 'nba_all'

df = pd.read_csv('../data/'+ file_name + '.csv', index_col=0)

update_date = df.iloc[len(df)-1]['DATE']
teams = list(df['HOME'].unique())






app = dash.Dash(__name__)

app.layout = html.Div([

                        ## HIDDEN DIVS: 

                        html.Div(id='hidden-div-update', style={'display': 'none'}),



						html.H1('NBA PREDICTIONS', style={'textAlign': 'center', 'backgroundColor': '#3E7ABF',
												        'color': 'white', 'height': '40px'}),

                        html.Div([
                            html.P('Last update: ' + str(update_date), id= 'update-date'),
                            html.Div([
                                html.P('Enter the Season'),
                                dcc.Input(id='input-season', type='text'),
                                html.P('Enter the Month'),
                                dcc.Input(id='input-month', type='text'),

                                ]),
                           
                            html.Button('Update', id='button'),



                            ]),

                        html.Div([
                            html.Div([
                                html.P('Select Home Team:'),
                                dcc.Dropdown(id='dropdown-home-team',
                                            options=[
                                                {'label': team, 'value': team} for team in teams]
                                                
                                            ,
                                            value=''),
                            ]),

                            html.Div([
                                html.P('Select  Visitor Team:'),
                                dcc.Dropdown(id='dropdown-visitor-team',
                                            options=[
                                                {'label': team, 'value': team} for team in teams]
                                                
                                            ,
                                            value=''),
                            ]),

                            html.Button('Compare', id='compare-button'),
                            dcc.Graph(id='output-graph',figure = ''),

                                ]),
								
								
						

			])
## Update DB with the button press
@app.callback(
    dash.dependencies.Output('hidden-div-update', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-season', 'value'), dash.dependencies.State('input-month', 'value')])
def update_output(n_clicks, season, month):

    print('Updating the DB...')
    NBA.update_db(season, month) 
    return ''



@app.callback(
    dash.dependencies.Output('output-graph', 'figure'),
    [dash.dependencies.Input('compare-button', 'n_clicks'),
    dash.dependencies.Input('dropdown-home-team', 'value'),
    dash.dependencies.Input('dropdown-visitor-team', 'value')],
    )
def update_output(n_clicks, home_team, visitor_team):

    fig = NBAF.get_team_data(df, home_team, visitor_team)


    return fig


if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', debug=True)