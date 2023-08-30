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

app.layout = html.Div([
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


if __name__ == '__main__':
    app.run(debug=True)
