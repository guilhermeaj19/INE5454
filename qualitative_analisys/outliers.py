import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from pathlib import Path

db_path = format(Path(__file__).parent.parent / "pharma.db")

engine = create_engine(f"sqlite:///{db_path}")

df = pd.read_sql("SELECT * FROM oferta", engine)

print(df.info())

# Boxplot para ver outliers
sns.boxplot(x=df['preco'])
plt.savefig("histograma_precos.png")
print("Gráfico salvo como histograma_precos.png")

# Filtrar valores extremos
# Exemplo: preços acima de 99 percentil
q99 = df['preco'].quantile(0.999)
print(f"99% dos preços são abaixo de: {q99}")

outliers = df[df['preco'] > q99]
print(outliers[['preco','url']])

print(df.loc[df['preco'] > 4000, ['url']])
