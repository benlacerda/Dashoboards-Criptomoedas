from plotly.graph_objects import Figure
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
from dash import dcc
import dash_daq as daq
import pandas as pd
import plotly_express as px


app = Dash(__name__)

### Graph Marketcap

df_btc = pd.read_csv('/Users/benjamim/PycharmProjects/DashAPC/venv/data/coin_Bitcoin.csv')
df_btc_array = df_btc.values
df_eth = pd.read_csv('/Users/benjamim/PycharmProjects/DashAPC/venv/data/coin_Ethereum.csv')
df_eth_array = df_eth.values

marketcap_btc = []
marketcap_eth = []
data = []

for linha_btc in df_btc_array:
    for linha_eth in df_eth_array:
        if linha_btc[3] == linha_eth[3]:
            marketcap_btc.append(linha_btc[9])
            marketcap_eth.append(linha_eth[9])
            data.append(linha_btc[3])

# eixo Y
media_marketcap = []
df_marketcap = pd.DataFrame(zip(marketcap_btc, marketcap_eth, data), columns=['marketcap-btc', 'marketcap-eth', 'data'])
df_marketcap['year']= pd.DatetimeIndex(df_marketcap['data']).year
contador = 0
while contador < len(df_marketcap):
    media_marketcap = (df_marketcap['marketcap-btc'] + df_marketcap['marketcap-eth']/2)
    contador = contador + 1

graph_marketcap = px.line(x=df_marketcap['data'], y=media_marketcap)

### Graph volume de transacoes

df_1 = pd.read_csv('/Users/benjamim/PycharmProjects/DashAPC/venv/data/AllCoin.csv')
df_array_1 = df_1.values

anos1 = []
volume = []
name = []

for linha in df_array_1:
    anos1.append(linha[3])
    volume.append(linha[8])
    name.append(linha[1])

lista_volume = list(zip(anos1,volume, name))
avaliable_names = df_1['Name'].unique()

graph_volume= px.histogram(lista_volume, x=anos1, y=volume, color=name)


# Layout
app.layout = html.Div([
    html.H1("Criptomoedas"),
    html.H3( "Grupo B"),

    html.Div(children=[
        dcc.Dropdown(
            id = 'dropdown',
            options=[{'label': i, 'value':i} for i in avaliable_names],value=['Bitcoin'], multi = False, placeholder = 'Filtre as moedas'
        ),# dropdown
        dcc.Graph(
            id = 'graph-volume'
        )# graph 1
    ])
])

# Callback do 1 graph
@app.callback(
    Output('graph-volume', 'figure'),
    Input('dropdown', 'value'))

def update_volume(value):
    ts = df_1[df_1["Name"].isin([value])]
    fig = px.histogram(ts, x="Date", y="Volume", color="Name")
    if value == None:
        fig_none = px.histogram( x="Date", y="Volume", color="Name")
        return fig_none
    fig.update_layout(title={'text': 'Comparação do volume de transações de várias criptomoedas',
                            'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'}),
    return fig

#roda o app
if __name__ == "__main__" :
    app.run_server(debug = True)