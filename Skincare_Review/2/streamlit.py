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
df = pd.read_csv('clean.csv')

df = df.dropna()

counts = df['author'].value_counts()

to_remove = counts[counts < 25].index.tolist()

df.drop(df[df['author'].isin(to_remove)].index, inplace=True)

# Streamlit APP

st.title('Produk SkinCare Rekomendasi')

Brand = st.selectbox('Brand',list(df['brand_name'].unique()))
df = df.loc[df['brand_name'].str.contains(Brand)]
# waktu = st.selectbox('Waktu', list(df['Waktu'].unique()))
# bulan = st.select_slider('Bulan', list(df['Bulan'].unique()))
# hari = st.select_slider('Hari', list(df['Hari'].unique()))


# def get_data(Waktu='', Bulan='', Hari=''):
#     global df
#     df= df.loc[
#         (df['Waktu'].str.contains(Waktu)) &
#         (df['Bulan'].str.contains(Bulan.title())) &
#         (df['Hari'].str.contains(Hari.title()))
#     ]
#     return df if filtered.shape[0] else 'Tidak Ditemukan'


# def user_input_features():
#     global rules
#     item = st.selectbox('Item', list(rules['antecedents'].unique()))
#     # waktu = st.selectbox('Waktu', list(df['Waktu'].unique()))
#     # bulan = st.select_slider('Bulan', list(df['Bulan'].unique()))
#     # hari = st.select_slider('Hari', list(df['Hari'].unique()))

#     # return item, waktu, bulan, hari

#     return item

# # item, waktu, bulan, hari = user_input_features()
# item = user_input_features()

# data = get_data(Waktu=waktu, Bulan=bulan, Hari=hari)

data = df

if type(data) != type('Tidak Ditemukan'):
    item_count_pivot = data.pivot_table(
        index='author', columns='product_title', values='product_rating', aggfunc='sum').fillna(0)
    item_count_pivot[item_count_pivot > 0] = 1

    freq = apriori(item_count_pivot, min_support=0.15, use_colnames=True)

    rules = association_rules(freq, metric='lift', min_threshold=1)
    rules.sort_values(by=['support', 'confidence', 'lift','conviction'], ascending=False, inplace=True)


def recommended_item(item_antecedents):
    if frozenset({item_antecedents}) in rules['antecedents'].unique():
        recom = rules.loc[rules['antecedents'] == frozenset(
            {item_antecedents}), 'consequents'].tolist()
        if len(recom[0]) > 1:
            return ' dan '.join(list(recom[0]))
        elif len(recom[0]) == 1:
            return str(list(recom[0])[0])
        else:
            return None

def user_input_features():
    global rules
    a = list(rules['antecedents'].unique())
    product_names = []

    for product in a:
        product_names += list(product)
    item = st.selectbox('Item', set(product_names))
    # waktu = st.selectbox('Waktu', list(df['Waktu'].unique()))
    # bulan = st.select_slider('Bulan', list(df['Bulan'].unique()))
    # hari = st.select_slider('Hari', list(df['Hari'].unique()))

    # return item, waktu, bulan, hari

    return item

# item, waktu, bulan, hari = user_input_features()
item = user_input_features()


if type(data) != type('Tidak Ditemukan'):
    if type(recommended_item(item)) == type("Character"):
        st.markdown('Hasil Rekomendasi Item : ')
        st.success(f'**{recommended_item(item)}**')
    else:
        st.markdown('Hasil Rekomendasi Item : ')
        st.error('Tidak Ada Rekomendasi Produk')
