import datetime
import os
import warnings

import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

from data_cleaning import *

warnings.filterwarnings("ignore")

#----------Preparing data------------------------------------------------------------
#df = pd.read_excel('D:\GeorgeLab\dashboard\output_clean.xlsx').drop('Unnamed: 0',axis=1)
#filepath = input("Enter File Path: ")
filepath = '/Users/yunyihuang/Documents/GL_github/gl_local/data/output_file_test.xlsx'
df = cleanup(filepath)
fname = df.Filename.iloc[0].split('\\')[-1]
initiated = df['Start Datetime'].min()
terminated = df['End Datetime'].max()

# transforming time
df_time = df.copy()
cols = df_time.columns.tolist()
cutoff = cols.index('Active 1')
time_begin = df_time['Start Datetime'].min().time()
time_to_minus = datetime.timedelta(hours=time_begin.hour,
                                   minutes=time_begin.minute,
                                   seconds=time_begin.second)

def tranform_to_time(row):
    start_time = row['Start Datetime']
    for col in cols[cutoff:]:
        secs = row[col]
        if secs != 0:
            row[col] = start_time + datetime.timedelta(seconds=secs) - time_to_minus
        else:
            pass
    return row

df_time = df_time.apply(tranform_to_time,axis=1)

stats = []
for i in range(16):
    test_row = df_time.iloc[i]
    for col in cols[cutoff:]:
        stat = []
        if (type(test_row[col]) != float) and (type(test_row[col]) != int):
            stat.append(test_row['Subject'])
            stat.append(test_row[col])
            stat.append(test_row[col] + datetime.timedelta(seconds=10))
            stat.append(col.split(' ')[0])
            stats.append(stat)
        else:
            pass

timeline_data = pd.DataFrame(stats,columns = ['Subject','Start','End','Type'])

#----------App layout----------------------------------------------------------------------
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY]) 
#server = app.server

app.layout = dbc.Container([
    
    html.Br(),
    html.Br(),
    dbc.Row([
       dbc.Col([
           dbc.Card([
               dbc.CardBody([
                   html.H1("Daily Analytics Dashboard", 
                            className="page-title", 
                            style={'textAlign':'center',
                                'fontWeight': 'bold'})
               ])
           ], color='primary', inverse=True)
       ]) 
    ]),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Dropdown(id='input_subject',
                 #className="dropdown-menu",
                 options=[{'label': x, 'value': x} for x in df["Subject"].unique()],
                 style={"width": "100%"},
                 placeholder = 'All Data',
                 searchable=False,
                 clearable=True),
            ], color='secondary', inverse=False)
        ], width=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('File Info'),
                    html.P("Filename: {}".format(fname)),
                    html.P("Started: {}".format(initiated)),
                    html.P("Ended: {}".format(terminated)),
                ], style={'textAlign':'center'})
            ], color='secondary', inverse=True),
        ], width=7),
    ],className='upper-info'),
    html.Br(),
    
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Active'),
                    html.H2(id='n_active')
                ], style={'textAlign':'center'})
            ], color='primary', inverse=True),
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Inactive'),
                    html.H2(id='n_inactive')
                ], style={'textAlign':'center'})
            ], color='primary', inverse=True),
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Reward'),
                    html.H2(id='n_reward')
                ], style={'textAlign':'center'})
            ], color='primary', inverse=True),
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Timeout'),
                    html.H2(id='n_timeout')
                ], style={'textAlign':'center'})
            ], color='primary', inverse=True),
        ], width=3),
        
    ],className="top-statistics"),
    
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Timelines', className="second-section-title"),
                    dcc.Graph(id='timeline')
                ], style={'textAlign':'center'})
            ]),
        ], width=12),
    ]),
    html.Br(),
    ])

#----------Callback for top statistics------------------------------------------------------------
@app.callback(
    [Output(component_id='n_active', component_property='children'),
     Output(component_id='n_inactive', component_property='children'),
     Output(component_id='n_reward', component_property='children'),
     Output(component_id='n_timeout', component_property='children')],
    [Input('input_subject','value')]
)

def update_statistics(input_subject):
    # when there is no subject chosen
    if input_subject is None:
        n_active = df['Active Lever Presses'].sum()
        n_inactive = df['Inactive Lever Presses'].sum()
        n_reward = df['Reward'].sum()
        n_timeout = df['Timeout'].sum()
    else:
        # filter by subject
        dff = df[df['Subject'] == input_subject]
        
        # get the statistics
        n_active = dff['Active Lever Presses'].values[0]
        n_inactive = dff['Inactive Lever Presses'].values[0]
        n_reward = dff['Reward'].values[0]
        n_timeout = dff['Timeout'].values[0]
        

    return n_active,n_inactive,n_reward,n_timeout



#----------Callback for timeline graphs------------------------------------------------------------
@app.callback(
    Output('timeline', 'figure'),
    Input('input_subject','value')
)

def update_timeline_graph(input_subject):
    # when there is no subject chosen
    if input_subject is None:
        dff = timeline_data
    else:
        dff = timeline_data[timeline_data['Subject'] == input_subject]
        
    timeline_graph = px.timeline(dff, 
                                 x_start="Start", 
                                 x_end="End", 
                                 y="Subject",
                                 color='Type')
    
    timeline_graph.update_xaxes(tickformat="%H:%M:%S",
                                tickformatstops=[dict(dtickrange=[1800000, 10800000], value="%H:%M")])
    
    timeline_graph.update_yaxes(categoryorder="category ascending")
    
    timeline_graph.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    
    return (timeline_graph)

#----------Run server----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(port=os.getenv('PORT', '8080'))
    #filepath = input("Enter File Path: ")
    app.run_server(debug=True)
