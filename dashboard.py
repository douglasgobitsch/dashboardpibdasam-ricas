from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO


url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY

template_theme1 = 'vapor'
template_theme2 = 'flatly'


df = pd.read_csv('gasolina.csv')
state_options = [{'label': x, 'value': x} for x in df['ESTADO'].unique()]


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme1, url_theme2]),
            html.H3('Preço x Estado'),
            dcc.Dropdown(
                id = 'estados',
                value = [state['label'] for state in state_options[:3]],
                multi = True,
                options = state_options
            ),
        ])
    ]),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'line_graph')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                id = 'estado1',
                value = state_options[0]['label'],
                options = state_options
                ), # pode usar o sm e o md aqui também
                dcc.Graph(id = 'indicator1'),
                dcc.Graph(id = 'box1')
            ])
        ]),

        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                id = 'estado2',
                value = state_options[1]['label'],
                options = state_options
                ),
                dcc.Graph(id = 'indicator2'),
                dcc.Graph(id = 'box2')
            ])
        ])
    ])
])


@app.callback(
    Output('line_graph', 'figure'),
    Input('estados', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def line(estados, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True) # isso é muito pesado mano, bora tentar melhorar isso
    mask = df_data['ESTADO'].isin(estados)

    fig = px.line(df_data[mask], x = 'DATA', y = 'PREÇO MÉDIO REVENDA', color = 'ESTADO', template = templates)

    return fig


@app.callback(
    Output('indicator1', 'figure'),
    Output('indicator2', 'figure'),
    Input('estado1', 'value'),
    Input('estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def indicators(estado1, estado2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)

    data_estado1 = df_data[df_data['ESTADO'].isin([estado1])]
    data_estado2 = df_data[df_data['ESTADO'].isin([estado2])]

    iterable = [(estado1, data_estado1), (estado2, data_estado2)]
    indicators = []

    for estado, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = 'number+delta',
            title = {'text': estado},
            value = data.at[data.index[-1], 'PREÇO MÉDIO REVENDA'],
            number = {'prefix': 'R$', 'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0], 'PREÇO MÉDIO REVENDA']}
        ))

        fig.update_layout(template = templates)
        indicators.append(fig)
    
    return indicators


@app.callback(
    Output('box1', 'figure'),
    Input('estado1', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box1(estado1, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_estado = df_data[df_data['ESTADO'].isin([estado1])]

    fig = px.box(data_estado, x = 'PREÇO MÉDIO REVENDA', template = templates, points='all', title=estado1)

    return fig


@app.callback(
    Output('box2', 'figure'),
    Input('estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box2(estado2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_estado = df_data[df_data['ESTADO'].isin([estado2])]

    fig = px.box(data_estado, x = 'PREÇO MÉDIO REVENDA', template = templates, points='all', title=estado2)

    return fig

if __name__ == '__main__':
    app.run_server(debug = True, port='8051')
