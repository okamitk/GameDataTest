from dash import html, dcc
import dash
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
load_figure_template(["cyborg"])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#========== Dados ============== #
df = pd.read_csv('vgsales.csv')
# Dados para os gráficos:

# Rank - Classificação das vendas gerais
# Name - O nome do jogo
# Platform - Plataforma de lançamento dos jogos (ou seja, PC, PS4, etc.)
# Year - Ano de lançamento do jogo
# Genre - Gênero do jogo
# Publisher - Editora do jogo
# NA_Sales - Vendas na América do Norte (em milhões)
# EU_Sales - Vendas na Europa (em milhões)
# JP_Sales - Vendas no Japão (em milhões)
# Other_Sales - Vendas no resto do mundo (em milhões)
# Global_Sales - Total de vendas mundiais.

df_genero = df.groupby('Genre').sum().reset_index()
df_total = df.groupby(['Global_Sales', 'Name'], sort=False).sum().head(10).reset_index()
df_agrupado_pelo_dia = df.groupby('Year', sort=False).agg({ 'Global_Sales': np.sum }).reset_index()
df_publicadoras_por_vendas = df.groupby(['Publisher', 'Year'], sort=False).agg({ 'Global_Sales': np.mean }).head(10).reset_index()
df_vendas_continentes = df.groupby(['Other_Sales', 'JP_Sales', 'EU_Sales', 'NA_Sales'], sort=False).agg({ 'Global_Sales': np.mean }).head(10).reset_index()
df_publicadoras_por_vendas = df.groupby(['Publisher', 'Year'], sort=False).agg({ 'Global_Sales': np.mean }).head(50).reset_index()

#Criação dos gráficos
mais_vendidos_fig = px.bar(df_total, x='Global_Sales', y='Name', color='Global_Sales') #Top 10 jogos e quanto eles venderam

vendas_genero_fig_pizza = px.pie(df_genero, values= 'Global_Sales',
       names='Genre', hole=.4) #Quantidade de vendas globais por gênero de jogo

vendas_ano_fig = px.bar(df_agrupado_pelo_dia, x='Year', y='Global_Sales') #Vendas por ano

vendas_regiao_fig= px.histogram(df_vendas_continentes, x=['Other_Sales', 'JP_Sales', 'EU_Sales', 'NA_Sales'], y='Global_Sales')
#O gráfico acima diz respeito a quantidade de vendas em cada continente.

vendas_editora_fig  = px.pie(df_publicadoras_por_vendas, values='Global_Sales', names='Publisher', hole=.4) #Vendas por editora


# =========  Layout  =========== #
app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(
            id="logo", 
            src=("https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Instituto_Federal_Marca_2015.svg/1200px-Instituto_Federal_Marca_2015.svg.png"),style={
                     "width":"auto",
                     "height":"4em",
                     "left":"50%",
                     "position":"relative",
                     "transform":"translateX(-50%)"
                     }),
        html.H2(children=[
            'Vendas de Jogos Eletrônicos'
        ]),
    ], style={
        "box-shadow":"""
            2.8px 2.8px 2.2px rgba(0, 0, 0, 0.02),
            6.7px 6.7px 5.3px rgba(0, 0, 0, 0.028),
            12.5px 12.5px 10px rgba(0, 0, 0, 0.035),
            22.3px 22.3px 17.9px rgba(0, 0, 0, 0.042),
            41.8px 41.8px 33.4px rgba(0, 0, 0, 0.05),
            100px 100px 80px rgba(0, 0, 0, 0.07)
        """,
        "backdrop-filter":"blur(10px)",
        "text-transform":"uppercase",
        "width":"fit-content",
        "margin":"auto",
        "font-family":"proxima-nova, sans-serif",
        "letter-spacing":"5px",
        "font-weight":"300",
        "font-size":"1em",
        "padding":"1em",
        "z-index":"2",
        "position":"relative",
        "border-radius":"10px"
        }),
    html.Div([
    html.H5(children=
            "Desenvolvedores: Bruno Jallon Moreira Alves, Francisco Felipe Vieira de Oliveira, Wálisson Andrey Sales Dutra."
            )], style={
                "background":"rgba(30, 30, 30, 0.5)",
                "box-shadow":"""
                    2.8px 2.8px 2.2px rgba(0, 0, 0, 0.02),
                    6.7px 6.7px 5.3px rgba(0, 0, 0, 0.028),
                    12.5px 12.5px 10px rgba(0, 0, 0, 0.035),
                    22.3px 22.3px 17.9px rgba(0, 0, 0, 0.042),
                    41.8px 41.8px 33.4px rgba(0, 0, 0, 0.05),
                    100px 100px 80px rgba(0, 0, 0, 0.07)
                """,
                "backdrop-filter":"blur(10px)",
                "margin": "25px", 
                "padding": "25px",
                "text-align": "center"
                }),
    dbc.Row([
        dbc.Col([
          dbc.Card([
            html.P("Menu de navegação",
                    className="fs-4 text-center mb-0"),
            html.Hr(), 
            html.P("Selecione o(s) genero(s)",
                    className="mb-0"),
                dbc.Checklist(
                    options=[{"label": x, "value": x} for x in df["Genre"].unique()], 
                    value=df["Genre"].unique(),
                    inline=True,
                    id="genero"),
                html.P("Selecione a(s) plataforma(s)",
                className="mb-0"),
                dcc.Dropdown(
                    df["Platform"].unique(),
                    df["Platform"].unique(),
                    id="plataforma",
                    multi=True
                ),
          ], className="p-2")  
        ],sm=3),

#Organização/apresentação dos Gráficos

        dbc.Col([
            dbc.Row([ 
                dbc.Col([
                    dcc.Graph(figure=mais_vendidos_fig,id="mais_vendidos_fig"),
                ], sm=4, className="me-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=vendas_ano_fig,id="vendas_ano_fig"),
                ], sm=4, className="ms-0 me-0 ps-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=vendas_regiao_fig,id="vendas_regiao_fig"),
                ], sm=4, className="ms-0 ps-0"),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=vendas_genero_fig_pizza,id="vendas_genero_fig_pizza"),
                ], sm=6, className="me-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=vendas_editora_fig, id="vendas_editora_fig")
                ], sm=6, className="ms-0 ps-0"),
            ])
        ],sm=9)
   ], style={
        "background":"url(https://images.unsplash.com/photo-1640340434855-6084b1f4901c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80)",
        "background-attachment":"fixed",
        "background-size":"cover",
        "background-repeat":"no-repeat",
        "margin":"0",
    })
])

@app.callback([
    Output("mais_vendidos_fig", "figure"),
    Output("vendas_ano_fig", "figure"),
    Output("vendas_regiao_fig", "figure"),
    Output("vendas_genero_fig_pizza", "figure"),    
    Output("vendas_editora_fig", "figure"),
],
    [
    Input("plataforma", "value"), Input("genero", "value")
])

def atualizar_graficos(plataforma, genero):
    #Atualizando o dataframe:    
    df_atualizado = df[(df["Platform"].isin(plataforma) & (df["Genre"].isin(genero)))]
    #Atualizando as variáveis:
    df_genero = df_atualizado.groupby('Genre').sum().reset_index()
    df_total = df_atualizado.groupby(['Global_Sales', 'Name'], sort=False).sum().head(10).reset_index()
    df_agrupado_pelo_dia = df_atualizado.groupby('Year', sort=False).agg({ 'Global_Sales': np.sum }).reset_index()
    df_publicadoras_por_vendas = df_atualizado.groupby(['Publisher', 'Year'], sort=False).agg({ 'Global_Sales': np.mean }).head(10).reset_index()
    df_vendas_continentes = df_atualizado.groupby(['Other_Sales', 'JP_Sales', 'EU_Sales', 'NA_Sales'], sort=False).agg({ 'Global_Sales': np.mean }).head(10).reset_index()
    df_publicadoras_por_vendas = df_atualizado.groupby(['Publisher', 'Year'], sort=False).agg({ 'Global_Sales': np.mean }).head(50).reset_index()
    #Atualizando os gráficos:
    mais_vendidos_fig = px.bar(df_total, x='Global_Sales', y='Name', color='Global_Sales')

    vendas_genero_fig_pizza = px.pie(df_genero, values= 'Global_Sales',
       names='Genre', hole=.4)

    vendas_ano_fig = px.bar(df_agrupado_pelo_dia, x='Year', y='Global_Sales')

    vendas_regiao_fig= px.histogram(df_vendas_continentes, x=['Other_Sales', 'JP_Sales', 'EU_Sales', 'NA_Sales'], y='Global_Sales')

    vendas_editora_fig  = px.pie(df_publicadoras_por_vendas, values='Global_Sales', names='Publisher', hole=.4)

    return mais_vendidos_fig, vendas_regiao_fig, vendas_genero_fig_pizza, vendas_ano_fig, vendas_editora_fig

if __name__ == "__main__":
    app.run_server(port=8051, debug=True)