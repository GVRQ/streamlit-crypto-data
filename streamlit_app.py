import requests
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Initialize Streamlit
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Creating a sidebar in Streamlit

crypto_name = st.sidebar.selectbox('Crypto coin', ('bitcoin', 'ethereum', 'bitcoin-cash', 'eos', 'stellar', 'litecoin', 'cardano', 'tether', 'iota', 'tron')) 
date_from = st.sidebar.date_input('Date from' ,datetime.date(2022, 12, 10))
date_to = st.sidebar.date_input('Date to' ,datetime.date(2023, 1, 10))

# Converting the date to UNIX format

date_from = int(datetime.datetime.combine(date_from, datetime.time.min).timestamp()*1000)
date_to = int(datetime.datetime.combine(date_to, datetime.time.max).timestamp()*1000)

# Getting data from the CoinCap API

url = f"https://api.coincap.io/v2/assets/{crypto_name}/history?interval=d1&start={date_from}&end={date_to}"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

json_data = json.loads(response.text.encode('utf8'))

crypto_data = json_data["data"]

# Writing data received from the Coinsup API to a CSV file
# Adding an additional column 'date' for the date in the "human format"

df = pd.DataFrame(crypto_data, columns=['time', 'priceUsd','date'])
df['time'] = (df['time']/1000).astype(int)
df['DATE'] = df['date'].astype(str)

time = []
for i in range(len(df)): 
    time = datetime.datetime.utcfromtimestamp(df['time'].values[i]).strftime('%Y-%m-%d')
    df['date'].values[i] = time

df['USD'] = pd.to_numeric(df['priceUsd'], errors='coerce').fillna(0, downcast='infer')
df.to_csv('crypto-exchange.csv', index=False)


# Open the csv file to import into Streamlit
crypto_exchange = pd.read_csv('crypto-exchange.csv')

# Creating a column in Streamlit
st.markdown('Cryptocurrency exchange rate')
st.bar_chart(crypto_exchange, x = 'DATE', y = 'USD')

# adding a section

st.markdown('Data is provided by the the Coinsup API and available for the following crypto coins: Bitcoin, Ethereum, Bitcoin-Cash, EOS, Stellar, Litecoin, Cardano, Tether, IOTA, TRON')
st.markdown("Text me on Telegram: https://t.me/gavrilov_se")
st.markdown("CV, Courses & Certificates: https://beacons.ai/gavrilov")