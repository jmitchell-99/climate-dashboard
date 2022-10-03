from dash import dcc, html
import dash_bootstrap_components as dbc
from plots import *

cplots = ClimatePlots()
fig_tc = cplots.temp_change()
fig_cd = cplots.carbon_dioxide()

def make_layout():
    """Design the layout of the dashboard."""

    layout = html.Div([
                dbc.Row([ 
                    dbc.Col( # LEFT COLUMN OF TABS
                        dcc.Tabs(id="tabs", children=[
                            dcc.Tab(label='Temperature', children=[dcc.Graph(id='wfig1', className="weather_fig")], className="tab", selected_className="tab_selected"),
                            dcc.Tab(label='Wind', children=[dcc.Graph(id='wfig2', className="weather_fig")], className="tab", selected_className="tab_selected"),
                            dcc.Tab(label='Rainfall', children=[dcc.Graph(id='wfig3', className="weather_fig")], className="tab", selected_className="tab_selected"),
                            dcc.Tab(label='Humidity', children=[dcc.Graph(id='wfig4', className="weather_fig")], className="tab", selected_className="tab_selected"),
                            dcc.Tab(label='Cloud', children=[dcc.Graph(id='wfig5', className="weather_fig")], className="tab", selected_className="tab_selected"),
                            dcc.Tab(label='UV Index', children=[dcc.Graph(id='wfig6', className="weather_fig")], className="tab", selected_className="tab_selected")]),
                            width=5),
                    dbc.Col([ # MIDDLE COLUMN OF 2 FIGURES
                        dbc.Col([
                            dbc.Col([ # LEFT COLUMN
                                dbc.Row([ # UPPER FIGURE ROW
                                    html.Div(dcc.Graph(id='cfig1', figure=fig_tc, className="climate_fig"))]),
                                html.Br(),
                                html.Br(),
                                dbc.Row([ # LOWER FIGURE ROW
                                    html.Div(dcc.Graph(id='cfig2', figure=fig_cd, className="climate_fig"))])
                                    ])])],
                        width=5),
                    dbc.Col([ # RIGHT COLUMN OF TEXT LABELS
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # LABEL 1 ROW
                            html.Div(children=[html.Label('Change Climate Plots:', className="input_label")])], justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # DROPDOWN 1 ROW
                            html.Div(children=[
                                dcc.Dropdown(
                                    id='dropdown1',
                                    options=[
                                        {'label': 'Temperature Change', 'value': 'fig_tc'},
                                        {'label': 'Carbon Dioxide', 'value': 'fig_cd'},
                                        {'label': 'Methane', 'value': 'fig_mt'},
                                        {'label': 'Nitrous Oxide', 'value': 'fig_no'},
                                        {'label': 'Polar Ice', 'value': 'fig_pi'}],
                                    value='fig_tc',
                                    clearable=False,
                                    className="dropdown",
                                    style={"backgroundColor": "#506784"})])], 
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # DROPDOWN 2 ROW
                            html.Div(children=[
                                dcc.Dropdown(
                                    id='dropdown2',
                                    options=[
                                        {'label': 'Temperature Change', 'value': 'fig_tc'},
                                        {'label': 'Carbon Dioxide', 'value': 'fig_cd'},
                                        {'label': 'Methane', 'value': 'fig_mt'},
                                        {'label': 'Nitrous Oxide', 'value': 'fig_no'},
                                        {'label': 'Polar Ice', 'value': 'fig_pi'}
                                    ],
                                    value='fig_cd',
                                    clearable=False,
                                    className="dropdown",
                                    style={"backgroundColor": "#506784"})])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        html.Br(style={'height': '1vh'}),    
                        dbc.Row([ # LABEL 3 ROW
                            html.Div(children=[html.Label('Find Country Average Weather:', className="input_label")])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # INPUT 2 ROW
                            html.Div(children=[dcc.Input(id='input2', placeholder='Enter a country...', type='text', className="input")])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row(html.Div(id='text10', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text11', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text12', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text13', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text14', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text15', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text16', className="label"), justify='center'),
                        dbc.Row(html.Div(id='text17', className="label"), justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row(html.Div(id='text18', className="label"), justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # LABEL 2 ROW
                            html.Div(children=[html.Label('Find Local Weather:', className="input_label")])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # INPUT 1a ROW
                            html.Div(children=[dcc.Input(id='input1a', placeholder='Enter a city...', type='text', className="input")])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ # 'EXTRA COUNTRY REQUIRED' ROW
                            html.Div(id='text0', className="label")],
                            justify='center'),
                        dbc.Row([ # INPUT 1b ROW
                            html.Div(children=[dcc.Input(id='input1b', placeholder="Enter the city's country...", type='text', className="input")])],
                            justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([html.Div(id='text1', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text2', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text3', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text4', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text5', className="label")], justify='center'), 
                        dbc.Row([html.Div(id='text6', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text7', className="label")], justify='center'),
                        dbc.Row([html.Div(id='text8', className="label")], justify='center'),
                        html.Br(style={'height': '1vh'}),
                        dbc.Row([ html.Div(id='text9', className="label")], justify='center')],
                        width=2) 
                ])
            ])

    return layout
