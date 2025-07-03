from engine import get_engine
import pandas as pd
from query_duplicated import get_ofertas_by_med_id_list

engine = get_engine()

# Medicamentos
def medicamentos_mesmo_nome(df):
  # Normaliza se precisar
  df['nome_normalizado'] = df['nome'].str.lower().str.strip()
  df['marca_normalizada'] = df['marca'].str.lower().str.strip()

  # Filtra todos os registros que aparecem mais de uma vez
  dupes = df[df.duplicated(subset=['nome_normalizado','marca_normalizada', 'is_generico'], keep=False)]

  print(dupes[['id', 'registro_ms', 'quantidade', 'nome', 'marca']].sort_values('nome'))

  return dupes['id'].tolist()


def medicamentos_linhas_duplicadas(df):
  ## Linhas inteiras ou o conjunto registro_ms e quantidade não são duplicados
  # Quantidade de linhas duplicadas (linha inteira igual)
  print(df.duplicated().sum())

  # Ver linhas duplicadas
  print(df[df.duplicated()])

  # Se quiser ver duplicatas por colunas específicas
  print(df[df.duplicated(subset=['registro_ms', 'quantidade'])])


# Ofertas
def ofertas_linhas_duplicadas(df):
  # Quantidade de linhas duplicadas (linha inteira igual)
  print(df.duplicated().sum())

  # Ver linhas duplicadas
  print(df[df.duplicated()])

  # Se quiser ver duplicatas por colunas específicas
  print(df[df.duplicated(subset=['url'])])

df_med = pd.read_sql("SELECT * FROM medicamento", engine)
df_oferta = pd.read_sql("SELECT * FROM oferta", engine)

duplicados = medicamentos_mesmo_nome(df_med)
get_ofertas_by_med_id_list(duplicados)
# medicamentos_linhas_duplicadas(df_med)
# ofertas_linhas_duplicadas(df_oferta)