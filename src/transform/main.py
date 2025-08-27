import pandas as pd
import sqlite3
from datetime import datetime
import re

# ------------------------
# Carregar JSON
# ------------------------
df = pd.read_json("../../data/data1.json")

# ------------------------
# Adicionar colunas fixas
# ------------------------
df['_source'] = df['url']
df['_datetime'] = datetime.now()

# ------------------------
# EXTRAÇÃO DA MARCA
# ------------------------
brands = ["Dell", "Acer", "Samsung", "Lenovo", "Asus", "HP", "Apple", "Positivo", "Vaio"]

def extract_brand(name):
    for brand in brands:
        if brand.lower() in str(name).lower():
            return brand
    return "Desconhecida"

df["brand"] = df["name"].apply(extract_brand)

# ------------------------
# TRATAMENTO DE PREÇOS
# ------------------------
for col in ['old_price', 'new_price']:
    if col in df.columns:
        # Remove tudo que não seja número ou vírgula/ponto
        df[col] = df[col].astype(str).str.replace(r'[^0-9,]', '', regex=True)
        # Substitui vírgula decimal por ponto
        df[col] = df[col].str.replace(',', '.')
        # Converte para float
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------
# TRATAMENTO DE REVIEWS
# ------------------------
if 'reviews_total' in df.columns:
    df['reviews_total'] = df['reviews_total'].astype(str).str.replace(r'[\(\)]', '', regex=True)
    df['reviews_total'] = pd.to_numeric(df['reviews_total'], errors='coerce').fillna(0).astype(int)

if 'reviews_rating' in df.columns:
    df['reviews_rating'] = pd.to_numeric(df['reviews_rating'], errors='coerce').fillna(0.0)

# ------------------------
# FILTRO DE PREÇOS
# ------------------------
df = df.dropna(subset=['old_price', 'new_price'])
df = df[
    (df['old_price'] >= 1000) & (df['old_price'] <= 10000) &
    (df['new_price'] >= 1000) & (df['new_price'] <= 10000)
]

# ------------------------
# SALVAR NO SQLITE
# ------------------------
conn = sqlite3.connect('../../data/mercadolivre2.db')
df.to_sql('notebooks', conn, if_exists='replace', index=False)
conn.close()

# ------------------------
# OUTPUT
# ------------------------
print(df.head())
