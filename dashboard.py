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


df = pd.read_csv('LiveLongerData.csv')
state_options = [{'label': x, 'value': x} for x in df['Sexos Afetados'].unique()]


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme1, url_theme2]),
            html.H3('Fatores de Longevidade de Vida'),
            dcc.Dropdown(
                id = 'sexos',
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
                id = 'sexo1',
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
                id = 'sexo2',
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
    Input('sexos', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def line(sexos, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True) # isso é muito pesado mano, bora tentar melhorar isso
    mask = df_data['Sexos Afetados'].isin(sexos)

    fig = px.line(df_data[mask], x = 'Fator', y = 'Anos Ganhos/Perdidos', color = 'Sexos Afetados', template = templates)

    return fig


@app.callback(
    Output('indicator1', 'figure'),
    Output('indicator2', 'figure'),
    Input('sexo1', 'value'),
    Input('sexo2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def indicators(sexo1, sexo2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)

    data_sexo1 = df_data[df_data['Sexos Afetados'].isin([sexo1])]
    data_sexo2 = df_data[df_data['Sexos Afetados'].isin([sexo2])]

    iterable = [(sexo1, data_sexo1), (sexo2, data_sexo2)]
    indicators = []

    for sexo, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = 'number+delta',
            title = {'text': sexo},
            value = data.at[data.index[-1], 'Anos Ganhos/Perdidos'],
            number = {'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0], 'Anos Ganhos/Perdidos']}
        ))
        
        fig.update_layout(template = templates)
        indicators.append(fig)
    
    return indicators


@app.callback(
    Output('box1', 'figure'),
    Input('sexo1', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box1(sexo1, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_sexo = df_data[df_data['Sexos Afetados'].isin([sexo1])]

    fig = px.box(data_sexo, x = 'Anos Ganhos/Perdidos', template = templates, points='all', title=sexo1)

    return fig


@app.callback(
    Output('box2', 'figure'),
    Input('sexo2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box2(sexo2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_sexo = df_data[df_data['Sexos Afetados'].isin([sexo2])]

    fig = px.box(data_sexo, x = 'Anos Ganhos/Perdidos', template = templates, points='all', title=sexo2)

    return fig

if __name__ == '__main__':
    app.run_server(debug = True, port='8051')