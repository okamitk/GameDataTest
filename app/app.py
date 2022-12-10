from dash import html, dcc
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import pandas as pd
import dash
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

load_figure_template(["cyborg"])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#========== Dados ============== #

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

# Carregando os dados usando pandas 
df = pd.read_csv('vgsales.csv')
df['Year'] = pd.to_datetime(df['Year'])
print(df.dtypes)

#Dados para os gráficos

df_classificacao= df.groupby('Rank').sum().reset_index()
df_nome= df.groupby('Name').sum().reset_index()
df_plataforma= df.groupby('Platform').sum().reset_index()
df_genero = df.groupby('Genre').sum().reset_index()
df_editora = df.groupby('Publisher').sum().reset_index()
df_vendas = df.groupby(['NA_Sales','EU_Sales','JP_Sales']).sum().reset_index()
df_resto = df.groupby('Other_Sales').sum().reset_index()
df_total = df.groupby('Global_Sales').sum().reset_index()

#Criação dos gráficos

vendas_fig = px.bar(df_total,x='Global Sales',y='Platform')
genero_fig = px.bar(df_genero, y="Genre",
                    x="Platform", color="Genre",orientation="h")

df_classificacao = px.bar(df_classificacao, x="Rank",
                    y="Name", color="Rank", orientation="h")

vendas_fig_pizza = px.pie(
        df_vendas, values='gross income', 
        names='City', hole=.4)

sexo_fig = px.pie(
        df_sexo, values='gross income', 
        names='Gender', hole=.4)

# =========  Layout  =========== #

app.layout = html.Div(children=[
    html.Img(id="logo", src=("https://nadic.ifrn.edu.br/static/img/part/ifpb.png"), height=85), 
    html.H1(children='Video Games Sales'),
    html.Div(children='''Este conjunto de dados contém uma lista de videogames com vendas superiores a 100.000 cópias. Foi gerado por uma raspagem de vgchartz.com'''),  
    html.P("""Utilize este dashboard para analisar vendas de video games"""),
    html.Div([
    html.H5(children=":D")], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
    
    dbc.Row([
        dbc.Col([
          dbc.Card([
            html.P("Menu de navegação",
                    className="fs-4 text-center mb-0"),
            html.Hr(), 
            html.P("Selecione a(s) cidade(s)",
                    className="mb-0"),
                dbc.Checklist(
                    options=[{"label": x, "value": x} for x in df["City"].unique()], 
                    value=df["City"].unique(),
                    inline=True,
                    id="checklist_city"),
                html.P("Selecione o período",
                    className="mb-0"),
                 dcc.DatePickerRange(
                    start_date=df["Date"].min(), end_date=df["Date"].max(), className="mb-2",
                    display_format="DD/MM/YYYY",
                    id="periodo"
                ),
                html.P("Selecione a(s) categoria(s)",
                className="mb-0"),
                dcc.Dropdown(
                    df["Product line"].unique(),
                    df["Product line"].unique(),
                    id="categoria",
                    multi=True
                ),
          ], className="p-2")  
        ],sm=3),

#Organização/apresentação dos Gráficos

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=vendas_fig,id="vendas_fig"),
                ], sm=4, className="me-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=pagamentos_fig,id="pagamentos_fig"),
                ], sm=4, className="ms-0 me-0 ps-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=df_classificacao,id="df_classificacao"),
                ], sm=4, className="ms-0 ps-0"),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=vendas_fig_pizza,id="vendas_fig_pizza"),
                ], sm=6, className="me-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=sexo_fig, id="sexo_fig")
                ], sm=6, className="ms-0 ps-0"),
            ])
        ],sm=9)
    ], className="p-2"),
])

#Callbacks

@app.callback([
    Output("vendas_fig", "figure"),
    Output("pagamentos_fig", "figure"),
    Output("df_classificacao", "figure"),
    Output("vendas_fig_pizza", "figure"),    
    Output("sexo_fig", "figure"),
],
    [
    Input("checklist_city", "value"),
    Input("periodo", "start_date"),
    Input("periodo", "end_date"),
    Input("categoria", "value"),

])
def atualizar_graficos(cidades, data_inicial, data_final, categoria):
    df_cidades = df[ (df["City"].isin(cidades)) & (df["Date"] >= data_inicial) & (df["Date"] <= data_final) & (df["Product line"].isin(categoria))]
     
    faturamento = df_cidades.groupby('City').sum().reset_index()
    pagamento = df_cidades.groupby('Payment').sum().reset_index()
    produtos = df_cidades.groupby(["Product line", "City"]).sum().reset_index()
    sexo = df_cidades.groupby(["Gender", "City"]).sum().reset_index()

    cidade_fig = px.bar(faturamento, x="City", y="gross income",
    )    
    pagamentos_fig = px.bar(pagamento, y="Payment",
                            x="gross income", orientation="h",
                            )    
    df_classificacao = px.bar(produtos, x="gross income",
                          y="Product line", color="City", 
                          orientation="h",
                          )        
    vendas_fig_pizza = px.pie(df_cidades, 
    values='gross income', names='City', hole=.4,
    )
    sexo_fig = px.pie(
        sexo, values='gross income', names='Gender', 
        title='Faturamento por sexo',  hole=.4,
        )
        

    return cidade_fig, pagamentos_fig, df_classificacao, vendas_fig_pizza, sexo_fig


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)