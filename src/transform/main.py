import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminho para o arquivo json
df = pd.read_json("data/data1.json")

# Setar o pandas para mostrar todas as colunas
# pd.options.display.max_columns = None

# Adicionar a coluna _source com um valor fixo
# df['_source'] = 'https://lista.mercadolivre.com.br/notebook'
# Adicionar a coluna _source com um valor real (url)
df['_source'] = df['url']

# Adicionar a coluna _source com um valor fixo
df["_datetime"] = datetime.now()

# Tratar os valores nulos para colunas numéricas e de texto

# Garantir que estão como string antes de usar .str
df['old_price'] = df['old_price'].astype(str).str.replace('.', '')
df['new_price'] = df['new_price'].astype(str).str.replace('.', '')
# Regex para remover os ( ):
df['reviews_total'] = df['reviews_total'].astype(str).str.replace(r'[\(\)]', '', regex=True)
# Remover os ( ) Sem regex (apenas string literal)
# df['reviews_total'] = df['reviews_total'].astype(str).str.replace('(', '').str.replace(')', '')

# Converter para numéricos
df['old_price'] = df['old_price'].astype(float)
df['new_price'] = df['new_price'].astype(float)
df['reviews_total'] = pd.to_numeric(df['reviews_total'], errors='coerce').fillna(0).astype(int)
#df['reviews_total'] = df['reviews_total'].astype(int)
df['reviews_rating'] = df['reviews_rating'].astype(float)

# Manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    (df['old_price'] >= 1000) & (df['old_price'] <= 10000) &
    (df['new_price'] >= 1000) & (df['new_price'] <= 10000)
]

# print(df['reviews_total'])

# Conectar (ou criar) banco local
conn = sqlite3.connect('data/mercadolivre.db')

# Salvar os dados em uma tabela
df.to_sql('notebooks', conn, if_exists='replace', index=False)

# Encerrar conexão
conn.close()



