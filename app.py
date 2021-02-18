import django
import django_heroku
import gunicorn
import os
import math
from flask import Flask
import pandas as pandas
import plotly.express as px
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq

colors = {'text': '#bdb477', 'background':'#090802'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])
server = app.server

def calc(vo2max, threshold, economy, race):
    vo2max = float(vo2max)
    threshold = float(threshold)
    economy = float(economy)
    race = float(race)
    emppace = economy/(vo2max*(threshold/100))
    metpace = emppace/1.609
    empmin = math.floor(emppace)
    empsec = round((emppace-empmin)*60, 0)
    metmin = math.floor(metpace)
    metsec = round((metpace-metmin)*60, 0)
    racetime = race*emppace
    racemin = racetime % 60
    racehour = (racetime - racemin)/60
    racesec = round((racemin % 1)*60, 0)
    racemin = "%02d"%racemin
    racesec = "%02d"%racesec
    empsec = "%02d"%empsec
    metsec = "%02d"%metsec
    return empmin, empsec, metmin, metsec, racehour, racemin, racesec



app.layout = html.Div([
    html.H1('Run Calculator', style = {'color':colors['text']}),
    html.H5('This calculator is designed to show the importance of the three biggest physiological metrics in endurance performance.\nUse the sliders to see how changes in one or more variables can affect your race time.', style = {'color':colors['text'],'textAlign': 'center'}),
    html.Br(),
    html.H4('VO2 Max (ml/kg/min)', style = {'color':colors['text']}),
    html.Br(),
    daq.Slider(id = 'vo2max', min = 0, max = 100, value = 65, handleLabel={"showCurrentValue": True,"label": "ml/kg/min",'color':colors['text']},  
        marks = {
            50: {'label':'Active', 'style':{'color':colors['text']}},
            65: {'label':'Very Fit', 'style':{'color': colors['text']}},
            80: {'label':'Elite', 'style':{'color': colors['text']}}
        }),
        html.Br(),
    html.H4('Threshold (percent of max)', style = {'color':colors['text']}),
    html.Br(),
    daq.Slider(id = 'threshold', min = 50, max = 100, value = 75, handleLabel={"showCurrentValue": True, 'label':'Percent', 'color':colors['text']},  
        marks = {
            65: {'label':'Low', 'style':{'color':colors['text']}},
            75: {'label':'Good', 'style':{'color': colors['text']}},
            85: {'label':'Exceptional', 'style':{'color': colors['text']}}
        }),
    html.Br(),
    html.H4('Running Economy (ml/kg/mile)', style = {'color':colors['text']}),
    html.Br(),
    html.Div([daq.Slider(id = 'economy', min = 300, max = 400, value = 350, handleLabel={"showCurrentValue": True,"label": "ml/kg/mile",'color':colors['text']},  
        marks = {
            325: {'label':'Elite', 'style':{'color':colors['text']}},
            350: {'label':'Good', 'style':{'color': colors['text']}},
            375: {'label':'Normal', 'style':{'color': colors['text']}}
        })]),
    html.Br(),
    html.H4('Race Distance', style = {'color':colors['text']}),
    html.Div([dcc.Dropdown(id = 'race', options = [
        {'label':'Marathon', 'value':26.2},
        {'label':'Half Marathon', 'value':13.1},
        {'label':'10K', 'value':6.21371}
    ], value = 26.2)],style={'padding-left':'2%','width':'50%'}),
    html.H3('Pace', style = {'color':colors['text']}),
    html.H3(id = 'paces', style = {'color':colors['text']}),
    html.Br(),
    html.H2(id = 'time', style = {'color':colors['text']})
], style = {'width':'100%','height':'100%', 'backgroundColor':colors['background'], 'margin':'0%'}
)

@app.callback(
    Output('paces','children'),
    Output('time','children'),
    Input('vo2max','value'),
    Input('threshold','value'),
    Input('economy','value'),
    Input('race','value')
)
def callback_pred(vo2max, threshold, economy, race): 
    pred = calc(vo2max = vo2max, threshold = threshold, economy = economy, race = race)
    return f'{pred[0]}:{pred[1]} per mile // {pred[2]}:{pred[3]} per kilometer', f'Race time: {int(pred[4])}:{pred[5]}:{pred[6]}'

if __name__ == '__main__':
    app.run_server(debug=False)
