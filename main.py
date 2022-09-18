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

# linha_btc[3] = date
# linha_eth[3] = date
# linha_eth[9] = marketcap


for linha_btc in df_btc_array:
    for linha_eth in df_eth_array:
        if linha_btc[3] == linha_eth[3]:
            marketcap_btc.append(linha_btc[9])
            marketcap_eth.append(linha_eth[9])
            data.append(linha_btc[3])

# eixo Y
media_marketcap = []

contador = 0
while contador < len(marketcap_btc):
    media_marketcap.append((marketcap_btc[contador] + marketcap_eth[contador])/2)
    contador = contador + 1

graph_marketcap = px.line(x=data, y=media_marketcap)

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

graph_volume= px.histogram(x=anos1, y=volume, color=name)

# Layout
app.layout = html.Div([
    html.H1("Criptomoedas"),
    html.H3( "Grupo B"),

    html.Div([
        dcc.Dropdown(
            id = 'dropdown',
            options=[{'label': i, 'value':i} for i in df_1.Name.unique()],multi = False, placeholder = 'Filtre as moedas'
        ),
        dcc.Graph(
            id = 'graph-volume'
        ),
        dcc.Graph(
            id = 'marketcap-graph',
            figure= graph_marketcap
        ),
    ])
])

@app.callback(
    Output('graph-volume', 'children'),
    Input('dropdown', 'value'))

def update_volume(dropdown_value):
    #filtered_volume = df_1[df_1.Name.str.contains('|'.join(dropdown_value))]
    #return graph_volume(filtered_volume)
    dff = df_1
    fig = graph_volume
    fig.update_layout(title={'text': 'Comparação do volume de transações de várias criptomoedas',
                             'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'})
    return fig

if __name__ == "__main__" :
    app.run_server(debug = True)