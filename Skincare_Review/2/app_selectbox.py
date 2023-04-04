import pandas as pd
import streamlit as st
from itertools import filterfalse

st.title('Analisis Produk Skincare Berdasarkan Review Pelanggan Menggunakan Algoritma Apriori')


df = pd.read_csv('Skincare_Review/2/nyka_top_brands_cosmetics_product_reviews.csv',sep=',')

df = df[['review_date','author','brand_name','product_title','price','review_rating','product_rating']]

# membuat pilihan yang tersedia
options = ['Olay', 'Nykaa Naturals', 'Nykaa Cosmetics', 'Nivea', 'NYX Professional Makeup', 'Maybelline New York', 'Lakme', "L'Oreal Paris", 'Kay Beauty', 'Herbal Essences']

# membuat multiselect dengan label "Select your favorite brands"
selected_options = st.multiselect('Select Brand Name :', options)

df = df.loc[df['brand_name'].isin(selected_options)]

rule = pd.read_csv('Skincare_Review/2/result_rules.csv',sep=',')

# Mengganti tanda kurung pada kolom 'items'
rule['antecedents'] = rule['antecedents'].apply(lambda x: [item.strip() for item in x.strip('()').split(',')])
rule['consequents'] = rule['consequents'].apply(lambda x: [item.strip() for item in x.strip('()').split(',') if item.strip() != ''])

product = set(df["product_title"].values)

product = set(df["product_title"].values)

product = sorted(list(product))

# Menyisipkan elemen None ke index 0
product.insert(0, None)


user_input = []

user_input.append(st.selectbox('Item 1',product,key='item1'))
user_input.append(st.selectbox('Item 2',product,key='item2'))
user_input.append(st.selectbox('Item 3',product,key='item3'))
user_input.append(st.selectbox('Item 4',product,key='item4'))

# user_input.append(st.text_input('Item 1',key='item1'))
# user_input.append(st.text_input('Item 2',key='item2'))
# user_input.append(st.text_input('Item 3',key='item3'))
# user_input.append(st.text_input('Item 4',key='item4'))

# user_input = list(filter(None, [s.strip('"') for s in user_input]))
user_input = list(filterfalse(lambda x: x is None, user_input))
user = sorted(user_input)

# st.markdown(type(user))

antecedents = rule['antecedents'].values
consequents = rule['consequents'].values

a = []
for i,v in enumerate(antecedents):
    a.append(sorted(antecedents[i]))

b = []
for i,v in enumerate(a):
    b.append([x for x in a[i] if x != ''])

for i,v in enumerate(b):
    c = [[s.replace("'", "") for s in inner] for inner in b]

d = []
for i,v in enumerate(c):
    d.append(sorted(c[i]))

# batas

e = []
for i,v in enumerate(consequents):
    e.append(sorted(consequents[i]))

f = []
for i,v in enumerate(e):
    f.append([x for x in e[i] if x != ''])

for i,v in enumerate(f):
    g = [[s.replace("'", "") for s in inner] for inner in f]


h = []
for i,v in enumerate(g):
    h.append((g[i]))

#batas
output = pd.DataFrame()
output['antecedents'] = c
output['consequents'] = g

if len(user) != 0:
    st.markdown('Pilihan Item :')
    st.info(user_input)
    target_items = set(user)

    if (output['antecedents'].apply(set) == target_items).any():
        hasil = output[output['antecedents'].apply(set) == target_items]
        st.markdown('Hasil Rekomendasi Item : ')
        st.success(hasil["consequents"].values[0])
    else:
        st.markdown('Hasil Rekomendasi Item : ')
        st.error('Tidak Ada Rekomendasi Produk')
else:
    st.markdown('Warning :')
    st.error('Silahkan Input Item!')





# # daftar opsi yang akan ditampilkan pada Selectbox
# options = ['option 1', 'option 2', 'option 3', 'option 4', 'option 5']

# # membuat input box untuk searching
# search_term = st.text_input('Search')

# # menyaring daftar opsi berdasarkan input pengguna
# filtered_options = [option for option in options if search_term.lower() in option.lower()]

# # menampilkan Selectbox dengan opsi yang sudah disaring
# selected_option = st.selectbox('Select an option', options=filtered_options, multiple=True)
