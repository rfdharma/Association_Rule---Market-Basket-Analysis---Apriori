import streamlit as st
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import locale
from mlxtend.frequent_patterns import association_rules, apriori


# Import Dataset
df = pd.read_csv('https://raw.githubusercontent.com/rfdharma/Association_Rule---Market-Basket-Analysis---Apriori/master/Minimarket_Indonesia/sales_detail.csv',sep=',')

# Data Pre-processing

# Convert Tipe Data
df['Price'] = df['Price'].astype(int)

# Pre-processing Date.Time
locale.setlocale(locale.LC_TIME, 'id_ID')
df['Date'] = pd.to_datetime(df['Date'])
df['Waktu'] = pd.cut(df['Hour'], bins=[0, 12, 18, 24],labels=['Pagi', 'Siang', 'Malam'])
df['Hari'] = df['Date'].dt.day_name(locale='id_ID')
df['Bulan'] = df['Date'].dt.month_name(locale='id_ID')
df['Tahun'] = df['Date'].dt.year


# Streamlit APP

st.title('Market Basket Analysis for Minimarket Indonesia')


def get_data(Waktu='', Bulan='', Hari=''):
    global df
    filtered = df.loc[
        (df['Waktu'].str.contains(Waktu)) &
        (df['Bulan'].str.contains(Bulan.title())) &
        (df['Hari'].str.contains(Hari.title()))
    ]
    return filtered if filtered.shape[0] else 'Tidak Ditemukan'


def user_input_features():
    global df
    item = st.selectbox('item', list(df['Product Name'].unique()))
    waktu = st.selectbox('waktu', list(df['Waktu'].unique()))
    bulan = st.select_slider('bulan', list(df['Bulan'].unique()))
    hari = st.select_slider('hari', list(df['Hari'].unique()))

    return item, waktu, bulan, hari


item, waktu, bulan, hari = user_input_features()

data = get_data(Waktu=waktu, Bulan=bulan, Hari=hari)


if type(data) != type('Tidak Ditemukan'):
    item_count_pivot = data.pivot_table(
        index='Receiveno', columns='Product Name', values='Qty', aggfunc='sum').fillna(0)
    item_count_pivot[item_count_pivot > 0] = 1

    freq = apriori(item_count_pivot, min_support=0.00001, use_colnames=True)

    rules = association_rules(freq, metric='lift', min_threshold=0.0001)
    rules.sort_values(by=['support', 'confidence', 'lift', 'conviction'], ascending=False, inplace=True)


def recommended_item(item_antecedents):
    if frozenset({item_antecedents}) in rules['antecedents'].unique():
        recom = rules.loc[rules['antecedents'] == frozenset(
            {item_antecedents}), 'consequents'].tolist()
        if len(recom[1]) > 1:
            return ' dan '.join(list(recom[1]))
        elif len(recom[1]) == 1:
            return str(list(recom[1])[0])
        else:
            return None


if type(data) != type('Tidak Ditemukan'):
    if type(recommended_item(item)) == type("Character"):
        st.markdown('Hasil Rekomendasi Item : ')
        st.success(f'**{recommended_item(item)}**')
    else:
        st.markdown('Hasil Rekomendasi Item : ')
        st.error('Tidak Ada Rekomendasi Produk')
