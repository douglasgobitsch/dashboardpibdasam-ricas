from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

df = pd.read_csv('treatedarchive.csv')
#lê o arquivo csv já tratado

app = Dash(__name__)

url_theme1 = dbc.themes.MORPH
url_theme2 = dbc.themes.SOLAR
template_theme1 = 'morph'
template_theme2 = 'solar'
#define os temas do site pra que sejam aplicados com mais facilidade nos gráficos

fig = px.bar(df, x="Ano", y="PIB (Dólares)", color="País", barmode="group")
opcoes = list(df['País'].unique())
opcoes.append("Todos os Países")
#define os valores do gráfico de barra e atribui os valores da coluna ao botão interativo

app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme1, url_theme2]),
            html.H1(children= 'PIB das Américas',
            style={'textAlign' : 'center'}), 
            html.H3(children= 'Uma dashboard feita por Douglas Gobitsch e Cauã Guerreiro.',
            style={'textAlign' : 'center'})
        ])
    ]),
    #escreve o cabeçalho do site
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(opcoes, value='Todos os Países', id='lista_países'),
        ])
    ]),
    #insere o botão dropdown
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])
    ]),
    #insere o gráfico de barra
   
   dbc.Row([
       dbc.Col([
           dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                df['Ano'].min(),
                df['Ano'].max(),
                step=None,
                value=df['Ano'].min(),
                marks={str(Ano): str(Ano) for Ano in df['Ano'].unique()},
                id='Ano-slider',
            )
       ])
   ]),
   #insere o gráfico de dispersão e o controle deslizante e define seus valores
])
@app.callback(
    Output('example-graph', 'figure'),
    Input('lista_países', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
#faz interação da troca de temas e do botão
def bar(value, toggle):
    templates = template_theme1 if toggle else template_theme2
    
    if value == "Todos os Países":
        fig = px.bar(df, x="Ano", y="PIB (Dólares)", color="País", barmode="group", template = templates)
    else:
        tabela_filtrada = df.loc[df['País']==value, :]
        fig = px.bar(tabela_filtrada, x="Ano", y="PIB (Dólares)", color="País", barmode="group", template = templates)
        
    fig.update_layout(template = templates)
    return fig
    #filtra os valores para que apareçam apenas valores de um só país e retorna esses valores atualizados




@callback(
    Output('graph-with-slider', 'figure'),
    Input('Ano-slider', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
#faz a interação do botão de troca de tema, para que o gráfico acompanhe a troca e a interação do controle deslizante
def scatter(selected_Ano, toggle):
    templates = template_theme1 if toggle else template_theme2
    
    filtered_df = df[df.Ano == selected_Ano]

    fig = px.scatter(filtered_df, x="PIB (Dólares)", y="População",
        size="Área do País", color="Continente", hover_name="País",
        log_x=True, size_max=55, template = templates)
    #define os valores do gráfico de dispersão
    
    fig.update_layout(transition_duration=500)
    #define o tempo de transição do gráfico quando muda de ano

    return fig


if __name__ == '__main__':
    app.run(debug=True)
#inicia o servidor do app no flask
