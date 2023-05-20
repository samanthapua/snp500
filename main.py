import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import streamlit as st

st.title('SNP 500')
st.sidebar.header('Input features')

@st.cache_data
def load_wiki_data(url_link):
    url = url_link
    content = pd.read_html(url, header=0)
    df = content[0]
    return df

snp_500 = load_wiki_data('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

sector = snp_500.groupby('GICS Sector')
unique_sector = sorted(snp_500['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector',unique_sector,unique_sector)

df_selected_sector = snp_500[snp_500['GICS Sector'].isin(selected_sector)]

st.header('Display companies in selected sectors')
st.dataframe(df_selected_sector)

data = yf.download(
        tickers = list(snp_500.Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )


def plot_graph(symbol,data):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date,df.Close,color='skyblue',alpha=0.3)
    plt.plot(df.Date, df.Close,color='skyblue',alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    return st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        plot_graph(i,data)