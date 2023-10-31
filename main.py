
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

# clean up the dataframe
ticker_df = clean_dataframe(ticker_df)

filtered_ticker_pairs = ticker_df.sort_values(
    by='volValue', ascending=False).head(20)


ticker_list = filtered_ticker_pairs['symbol'].tolist()
print(ticker_list)
# streamlit app
latest_iteration = st.empty()

latest_iteration.markdown("*Kucoin **Crypto dashboard** *")


bar = st.progress(len(ticker_list))
# getting market data
orderbook_data = {}
candle_data = {}
market_data = {}
i = 0
for key in ticker_list:
    print(key)

    df_market = marketstatspull(key)
    bar.progress(i)
    i += 1
    market_data[key] = df_market
    latest_iteration.markdown(
        f'Fetching latest :blue[market data] stats for: :rainbow[{key}]')
    print(df_market.shape)

    df_orderbook = orderbookpull(key)
    bar.progress(i)

    orderbook_data[key] = df_orderbook
    latest_iteration.markdown(
        f'Fetching latest :blue[orderbook data] for: :rainbow[{key}]')
    print(df_orderbook.shape)

    df_candle = main_candle(key)
    bar.progress(i)

    candle_data[key] = df_candle
    latest_iteration.markdown(
        f'Fetching latest :blue[candle data] for : :rainbow[{key}]')
    print(df_candle.shape)


# This needs to be a conditional
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
            tickformat=":,.2f"
        )
    )
    st.plotly_chart(fig, use_container_width=True)


with st.container():

    st.header('Candle Plot - Daily')
    st.divider()

    tab_labels = st.selectbox("Select Ticker Pair", ticker_list)
    # Iterate over the list and create tabs
    # Ticker mapping

    ticker_mapping = {item: item for item in ticker_list}

    if tab_labels in ticker_mapping:
        selected_ticker_pair = ticker_mapping[tab_labels]
        plot_candlestick(selected_ticker_pair)
    else:
        st.write("Invalid selection")
# -------------------------Side Bare -------------------------#

# Sidebar
# Using object notation


# Using "with" notation
with st.sidebar:
    st.subheader('Dashboard Summary and build.', divider='rainbow')
    st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors].\n
    This code is a Streamlit app that pulls market data from the Kucoin exchange API and displays it in a dashboard. 
                The app imports various libraries such as Streamlit, Pandas, Plotly, and requests.
                 It also imports functions from a custom module called "dataextraction" for extended data manipulation. 
                The app starts by fetching all tickers from the Kucoin API and cleaning up the resulting dataframe.
                 It then selects the top 20 tickers by volume and fetches market data, orderbook data, 
                and candle data for each ticker. The app then displays a candlestick plot for the selected 
                ticker pair and allows the user to select which ticker information to display.
                ''')


# ------------------------------- Data Bar Set Below -------------------------------#

# append data
market_data_appended_df = pd.concat(
    market_data.values(), ignore_index=True)

market_data_appended_df['datetime'] = pd.to_datetime(
    market_data_appended_df['time'], unit='ms')
market_data_appended_df.set_index('datetime', inplace=True)
trade_url = 'https://www.kucoin.com/trade/'

market_data_appended_df['Trade'] = trade_url + \
    market_data_appended_df['symbol']

# object formating


def convert_data_types(df):
    # def convert_to_string(df_):
    #     string_columns = ['symbol', 'symbolName']
    #     return df_.apply(pd.to_string, subset=string_columns)   #astype(str)

    def convert_to_float(df_):
        float_columns = ['buy', 'sell', 'changeRate', 'changePrice', 'high', 'low',
                         'vol', 'volValue', 'last', 'averagePrice', 'takerFeeRate', 'makerFeeRate']
        return df_.apply(pd.to_numeric, errors='coerce', downcast='float')

    def convert_to_int(df_):
        int_columns = ['takerCoefficient', 'makerCoefficient']
        return df_.apply(pd.to_numeric, errors='coerce', downcast='integer')

    return (df
            .pipe(convert_to_float)
            # .pipe(convert_to_int)
            )


market_data_appended_converted_df = convert_data_types(market_data_appended_df)

# style - formating
market_data_styled_df = market_data_appended_converted_df.style.format({
    'buy': '{:,.8f}'.format,
    'sell': '{:,.8f}'.format,
    'changeRate': '{:,.2%}'.format,
    'changePrice': '{:,.8f}'.format,
    'high': '{:,.8f}'.format,
    'low': '{:,.8f}'.format,
    'vol': '{:,.8f}'.format,
    'volValue': '{:,.8f}'.format,
})


orderbook_data_appended_df = pd.concat(
    orderbook_data.values(), ignore_index=True)
# market_data_appended_df_sorted = market_data_appended_df.sort_values(
#     'date', ascending=False)


with st.container():
    # This container is for the line data from market stats
    options = st.multiselect(
        'Select Ticker information to display',
        filtered_ticker_pairs)

    # my_table = st.table(market_data['ETHUP-USDT'])
    # market_data_appended_df['changeRate'] = market_data_appended_df['changeRate'].apply(
    #     lambda x: f"{x:.2%}")
    st.dataframe(market_data_appended_df[[
                 'symbol',	'buy',	'sell',	'changeRate',	'changePrice',	'high',	'low',	'vol',	'volValue', 'Trade']], column_config={
        'symbol': {'width': 80},
        'buy': {'width': 80},
        'sell': {'width': 80},
        'changeRate': {'width': 80},
        'changePrice': {'width': 80},
        'high': {'width': 58},
        'low': {'width': 50},
        'vol': {'width': 50},
        'volValue': {'width': 50},
        'Trade': st.column_config.LinkColumn("Trade on Kucoin",
                                             help="Trade on Kucoin",
                                             validate="^https://[a-z]+\.streamlit\.app$")}
    )

    # filter by latest date s
