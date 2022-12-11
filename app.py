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
load_figure_template(["flatly"])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

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
df_classificacao = df.groupby('Rank').sum().reset_index()
df_nome = df.groupby('Name').sum().reset_index()
df_plataforma = df.groupby('Platform').sum().reset_index()
df_genero = df.groupby('Genre').sum().reset_index()
df_editora = df.groupby('Publisher').sum().reset_index()
df_vendas = df.groupby(['NA_Sales','EU_Sales','JP_Sales']).sum().reset_index() #Esse
df_resto = df.groupby('Other_Sales').sum().reset_index() #Esse
df_total = df.groupby(['Global_Sales', 'Name'], sort=False).sum().head(10).reset_index() #Esse
df_agrupado_pelo_dia = df.groupby('Year', sort=False).agg({ 'Global_Sales': np.sum }).reset_index()
df_publicadoras_por_vendas = df.groupby(['Publisher', 'Year'], sort=False).agg({ 'Global_Sales': np.mean }).head(10).reset_index()
print(df_total)
#Criação dos gráficos

# cidades_fig = px.bar(df_editora,x='Publisher',y='Global_Sales')
# gross income = renda bruta

#cidades_fig = px.line(df_publicadoras_por_vendas , x='Publisher', y='Global_Sales', color='Global_Sales') #Gráfico de linha
cidades_fig = px.bar(df_total, x='Global_Sales', y='Name', color='Global_Sales')

# cidades_fig = px.scatter(df_publicadoras_por_vendas, x="Global_Sales", y="Publisher",
#                  size="Global_Sales", color="Global_Sales", hover_name="Publisher",
#                  log_x=True, size_max=60) #Gráfico com bolinha
vendas_fig_pizza = px.pie(df_genero, values= 'Global_Sales',
        names='Genre', hole=.4) #Quantidade de vendas globais por gênero de jogo

sexo_fig = px.bar(df_agrupado_pelo_dia, x='Year', y='Global_Sales') #Vendas por ano
#cidades_fig = px.bar(df_plataforma, x= 'Platform', y='Global_Sales', color='Global_Sales')

# pagamentos_fig = px.bar(df_pagamentos, y="Payment",
#                       x="gross income", color="Payment",orientation="h")



# sexo_fig = px.pie(
#         df_agrupado_pelo_dia, values='JP_Sales',
#         names='Year', hole=.4)


# =========  Layout  =========== #
app.layout = html.Div(children=[
    dbc.Row([
        #Primeira coluna:
        dbc.Col([
            dbc.Card( #Cria uma estrutura ao seu redor (por isso é melhor)
                dbc.CardBody([
                    html.H4("Dashboard de Vendas"),
                    html.Hr(),
                    # dcc.Checklist(df['City'].unique(), df['City'].unique(), 
                    #     id="checklist_city"),
                ]), style=({"padding":"10px"})
            )
        ], width=3), #termina aqui
        #Segunda coluna
        dbc.Col([
            dbc.Row([
                html.H3("Relatório de Faturamento",style={'text-align':'center'}),
                html.Hr(),
                dbc.Col([
                    dcc.Graph(figure=cidades_fig,id="cidades_fig"),
                ]),
                # dbc.Col([
                #     dcc.Graph(figure=pagamentos_fig,id="pagamentos_fig"),
                # ]),
                # dbc.Col([
                #     dcc.Graph(figure=produtos_fig,id="produtos_fig"),
                # ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=vendas_fig_pizza,id="vendas_fig_pizza"),
                ]),
                dbc.Col([
                    dcc.Graph(figure=sexo_fig, id="sexo_fig")
                ])
            ]),
        ], width=9)
    ]),
       
])

#Callbacks - Decorador (altera o comportamento de uma função)
#Você escolhe a output/saída (o que eu vou atualizar)
#Cada componente tem uma id para que ele possa ser identificado
@app.callback([
    Output("cidades_fig", "figure"),
    Output("pagamentos_fig", "figure"),
    Output("produtos_fig", "figure"),
    Output("vendas_fig_pizza", "figure"),    
    Output("sexo_fig", "figure"),
],
    [
    Input("checklist_city", "value")
    #checklist retorna os valores
])
def atualizar_graficos(cidades):
    df_cidades = df[df["City"].isin(cidades)]
    #Atualizou o dataframe
    faturamento = df_cidades.groupby('City').sum().reset_index()
    pagamento = df_cidades.groupby('Payment').sum().reset_index()
    produtos = df_cidades.groupby(["Product line", "City"]).sum().reset_index()
    sexo = df_cidades.groupby(["Gender", "City"]).sum().reset_index()
    #Atualizou as variáveis
    cidade_fig = px.bar(faturamento, x="City", y="gross income")  
    pagamentos_fig = px.bar(pagamento, y="Payment",
                            x="gross income", orientation="h")    
    produtos_fig = px.bar(produtos, x="gross income",
                          y="Product line", color="City", 
                          orientation="h")        
    vendas_fig_pizza = px.pie(df_cidades, 
    values='gross income', names='Gender', hole=.4)
    sexo_fig = px.pie(
        sexo, values='gross income', names='Gender', 
        title='Faturamento por sexo',  hole=.4)

    return cidades_fig, pagamentos_fig, produtos_fig, vendas_fig_pizza, sexo_fig
    #A quantidade de retornos tem que ser igual a quantidade de output

if __name__ == "__main__":
    app.run_server(port=8051, debug=True)