import dash
from dash_bootstrap_components._components.FormGroup import FormGroup
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd 
import yfinance as yf
import plotly.express as px
import numpy as np
from statistics import NormalDist 

# prepare the app for plotting
app = dash.Dash(
    external_stylesheets=[dbc.themes.SIMPLEX]
)


# bootstrap layout

layout = dbc.Container([
    dbc.Row([dbc.Col(dbc.Jumbotron([html.H1("How extreme is the move?"),
    html.H5("""A little app to help you figure out how extreme the move of a stock price is."""),
    dcc.Markdown("""The graph below shows the historical daily percentage changes of the stock from one day's close to
    the next day's close. You can use the dropdown menu to choose if you want to use intra-day (i.e. open to close) 
    percentage changes or inter-day (i.e. close to close) movements."""),
    dcc.Markdown("_Data Source: Yahoo Finance_")]))]),
    dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Choose your ticker"),
                    dbc.Input(
                        type="text",
                        id="input",
                        placeholder="Ticker",
                    ),
                ]
            ),
            width=5,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Daily percentage change"),
                    dbc.Input(
                        type="number",
                        id="perc_chg",
                        placeholder="Percentage Change",
                    ),
                ]
            ),
            width=5,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Type of change"),
                    dcc.Dropdown(
                        id = "drop",
                        options = [{'label':'Intra-Day', 'value':'0'},
                        {"label":'Inter-day', "value":"1"}]
                    ),
                ]
            ),
            width=2,
        ),
    ],
    form=True,
),
    dbc.Row(dbc.Col(dbc.Button("Submit", id="butt", color="primary", className="mr-1"))),
    dbc.Row(dbc.Col(html.H3(id="outputs"), width={"offset":4})),
    dbc.Row([dbc.Col(dcc.Graph(id="example"))])
])

app.layout = layout

@app.callback(
    Output('example', 'figure'),
    Output('outputs', 'children'),
    Input("butt", "n_clicks"),
    [State("drop", "value"),
    State('input', 'value'),
    State('perc_chg', 'value')])
def return_value(n_clicks, type, value, value2):

    # change the function based on whether inter or intra day is selected

    if type == "1":
        # first part of the function to display graph
        ticker = value
        SPY =yf.download(ticker)
        SPY['Adj Close'] = SPY['Adj Close'].pct_change()*100
        SPY.reset_index(inplace=True)
        SPY['Date_str'] = SPY['Date'].astype(str)
        fig = px.strip(SPY.reset_index(), x = 'Adj Close', orientation='h',
        labels={"variable":" ", "value":"Percentage Change"},
        title=f"Daily Percentage Change of {ticker}", hover_data=['Adj Close', 'Date_str'], template="ggplot2")
        fig.update_traces(jitter = 0.5).update_yaxes(range=[-0.13,0.13]).update_xaxes(nticks=16)

        # second part of function to display the stat difference

        perc_change = SPY['Adj Close']

        user_move = value2
        if user_move > 0: 
            prob = 1 - NormalDist(sigma=np.std(perc_change), mu=np.mean(perc_change)).cdf(user_move)
            display = f"The probability it moves {user_move}% inter-day is {round(prob,3)}"

        elif user_move < 0: 
            prob = NormalDist(sigma=np.std(perc_change), mu=np.mean(perc_change)).cdf(user_move)
            display = f"The probability it moves {user_move}% inter-day is {round(prob,3)}"

        return(fig, display)

    elif type == "0":
        # first part of the function to display graph
        ticker = value
        SPY =yf.download(ticker)
        SPY['Intraday Change'] = ((SPY["Open"] - SPY["Close"])/SPY["Open"]*100)
        SPY.reset_index(inplace=True)
        SPY['Date_str'] = SPY['Date'].astype(str)
        fig = px.strip(SPY.reset_index(), x = 'Intraday Change', orientation='h',
        labels={"variable":" ", "value":"Percentage Change"},
        title=f"Daily Percentage Change of {ticker}", hover_data=['Intraday Change', 'Date_str'], template="ggplot2")
        fig.update_traces(jitter = 0.5).update_yaxes(range=[-0.13,0.13]).update_xaxes(nticks=16)

        # second part of function to display the stat difference

        perc_change = SPY['Intraday Change']

        user_move = value2
        if user_move > 0: 
            prob = 1 - NormalDist(sigma=np.std(perc_change), mu=np.mean(perc_change)).cdf(user_move)
            display = f"The probability it moves {user_move}% intra-day is {round(prob,3)}"

        elif user_move < 0: 
            prob = NormalDist(sigma=np.std(perc_change), mu=np.mean(perc_change)).cdf(user_move)
            display = f"The probability it moves {user_move}% intra-day is {round(prob,3)}"

    
        return(fig, display)

if __name__ == '__main__':
    app.run_server(debug=True) 
