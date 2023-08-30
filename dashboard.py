from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

df = pd.read_csv('Data_America.csv')

# Tratar valores nulos em colunas numéricas (preenchendo com a média)
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_columns:
    mean_value = df[col].mean()
    df[col].fillna(mean_value, inplace=True)

# Tratar valores nulos em colunas categóricas (preenchendo com o valor mais frequente)
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    most_common_value = df[col].mode()[0]
    df[col].fillna(most_common_value, inplace=True)

# O DataFrame 'df' agora está com os valores nulos tratados

app = Dash(__name__)

colors = {
    'background': '#FFDEAD',
    'text': '#191970'
}

fig = px.bar(df, x="Year", y="GDP (USD)", color="Country", barmode="group")
opcoes = list(df['Country'].unique())
opcoes.append("Todos os Países")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children= 'PIB das Américas',
    style={'color': colors['text']}
    ), 
    html.H2(children= 'Uma dashboard feita por Douglas Gobitsch e Cauã Guerreiro.',
    style={'color': colors['text']}
    ),
    
    dcc.Dropdown(opcoes, value='Todos os Países', id='lista_países'),
    
    dcc.Graph(
    id='example-graph',
    figure=fig
    ),
   
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        value=df['Year'].min(),
        marks={str(Year): str(Year) for Year in df['Year'].unique()},
        id='Year-slider'
    )
])
@app.callback(
    Output('example-graph', 'figure'),
    Input('lista_países', 'value')
)
def update_output(value):
    if value == "Todos os Países":
        fig = px.bar(df, x="Year", y="GDP (USD)", color="Country", barmode="group")
    else:
        tabela_filtrada = df.loc[df['Country']==value, :]
        fig = px.bar(tabela_filtrada, x="Year", y="GDP (USD)", color="Country", barmode="group")
    return fig


@callback(
    Output('graph-with-slider', 'figure'),
    Input('Year-slider', 'value'))
def update_figure(selected_Year):
    filtered_df = df[df.Year == selected_Year]

    fig = px.scatter(filtered_df, x="GDP (USD)", y="Population ",
                     size="Country area (km^2)", color="Continent", hover_name="Country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

if __name__ == '__main__':
    app.run(debug=True)
