
# Importing the libraries

import streamlit.components.v1 as components
from dataextraction import *
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime
import plotly as py
import warnings  # this is to ignore warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

# Streamlit components


# Importing the dataset
# uploading of dataset


st.title('Kucoin Crypto Dashboard Demo')
st.divider()
# set up ticking datatickers = requests.get('https://api.kucoin.com/api/v1/market/allTickers')
tickers = requests.get('https://api.kucoin.com/api/v1/market/allTickers')
tickers = tickers.json()
tickers = tickers['data']['ticker']
ticker_df = pd.DataFrame(tickers)
filtered_ticker_pairs =ticker_df.sort_values(by='vol', ascending=False).head(20)


ticker_list = ticker_df['symbol'].tolist()

# streamlit app
latest_iteration = st.empty()

latest_iteration.markdown("*Kucoin **Crypto dashboard** *")


latest_iteration.markdown('''
    Pulling data from the Kucoin API and displaying it in a dashboard.
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors].''')

bar = st.progress(len(filtered_ticker_pairs)*3)
# getting market data
market_data = {}
i = 0
for key in filtered_ticker_pairs:

    df = marketstatspull(key)
    bar.progress(i)
    i += 1
    market_data[key] = df
    latest_iteration.text(
        f'Fetching latest market stats data for Ticker Pair :{key}')

orderbook_data = {}

for key in filtered_ticker_pairs:
    df = orderbookpull(key)
    bar.progress(i)
    i += 1
    orderbook_data[key] = df
    latest_iteration.text(
        f'Fetching latest orderbook data for Ticker Pair :{key}')

candle_data = {}

for key in filtered_ticker_pairs:
    df = main_candle(key)
    bar.progress(i)
    i += 1
    candle_data[key] = df
    latest_iteration.text(
        f'Fetching latest candle data for Ticker Pair :{key}')


st.success('''
    :red[Data ] :orange[download] :green[is] 
    :rainbow[DONE].''', icon="✅")

bar.empty()
latest_iteration.empty()

# ---------------------------- We have our complete data now ----------------------------#

# ---------------------------- Data Bar Set Below ----------------------------#

def plot_candlestick(ticker_pair):
    st.header(ticker_pair)
    fig = go.Figure(
        data=[go.Candlestick(
            x=candle_data[ticker_pair]['date'],
            open=candle_data[ticker_pair]['open'],
            high=candle_data[ticker_pair]['high'],
            low=candle_data[ticker_pair]['low'],
            close=candle_data[ticker_pair]['close']
        )],
    )
    fig.update_layout(
        yaxis=dict(
            tickformat=".2f"
        )
    )
    st.plotly_chart(fig, use_container_width=True)


with st.container():

    st.header('Candle Plot - Daily')
    st.divider()

    
    tab_labels=st.selectbox("Select Ticker Pair", filtered_ticker_pairs)
    # Iterate over the list and create tabs
    
       
    match tab_labels:
        case "LTC3L-USDT":
            plot_candlestick('LTC3L-USDT')
        case "BCH-USDT":
            plot_candlestick('BCH-USDT')
        case "LTC3S-USDT":
            plot_candlestick('LTC3S-USDT')
        case "BTC3L-USDT":
            plot_candlestick('BTC3L-USDT')
        case "ETH3S-USDT":
            plot_candlestick('ETH3S-USDT')
        case "BTC3S-USDT":
            plot_candlestick('BTC3S-USDT')
        case "ETH3L-USDT":
            plot_candlestick('ETH3L-USDT')
        case "BTC-USDT":
            plot_candlestick('BTC-USDT')
        case "XRP3S-USDT":
            plot_candlestick('XRP3S-USDT')
        case "BTCDOWN-USDT":
            plot_candlestick('BTCDOWN-USDT')
        case "XRP3L-USDT":
            plot_candlestick('XRP3L-USDT')
        case "BCHSV-USDT":
            plot_candlestick('BCHSV-USDT')
        case "ETH-USDT":
            plot_candlestick('ETH-USDT')
        case "BTCUP-USDT":
            plot_candlestick('BTCUP-USDT')
        case "XRP-USDT":
            plot_candlestick('XRP-USDT')
        case "ETHUP-USDT":
            plot_candlestick('ETHUP-USDT')
        case "ETHDOWN-USDT":
            plot_candlestick('ETHDOWN-USDT')
        case "LTC-USDT":
            plot_candlestick('LTC-USDT')
        case "BCH3L-USDT":
            plot_candlestick('BCH3L-USDT')
        case "ETHW-USDT":
            plot_candlestick('ETHW-USDT')
        case "BCH3S-USDT":
            plot_candlestick('BCH3S-USDT')



# -------------------------Side Bare -------------------------#

# Sidebar
# Using object notation


# Using "with" notation
with st.sidebar:
    st.subheader('This is a subheader with a divider', divider='rainbow')
    st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors].''')


# ------------------------------- Data Bar Set Below -------------------------------#

# append data
market_data_appended_df = pd.concat(
    candle_data.values(), ignore_index=True)

market_data_appended_df_sorted = market_data_appended_df.sort_values(
    'date', ascending=False)
market_data_latest_date = market_data_appended_df_sorted.iloc[0]


with st.container():
    # This container is for the line data from market stats
    options = st.multiselect(
        'Select Ticker information to display',
        filtered_ticker_pairs)

    my_table = st.table(market_data['ETHUP-USDT'])

    # filter by latest date
