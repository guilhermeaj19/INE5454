from sqlalchemy import create_engine, inspect
from engine import get_engine
import pandas as pd
from pathlib import Path

engine = get_engine()

# Lista tabelas
inspector = inspect(engine)
print("Tabelas:", inspector.get_table_names())

# 4. Carrega uma tabela
df = pd.read_sql("SELECT * FROM medicamento", engine)

# 5. Inspeciona
print(df.info())
# print(df.head())

# Quantidade total de nulos por coluna
print(df.isnull().sum())

# Porcentagem de nulos
print(df.isnull().sum() / len(df) * 100)

# Ver linhas com muitos nulos
print(df[df.isnull().any(axis=1)])

# df = pd.read_sql("SELECT * FROM oferta", engine)

# print(df.info())
# print(df.head())

# df = pd.read_sql("SELECT * FROM farmacia", engine)

# print(df.info())
# print(df.head())