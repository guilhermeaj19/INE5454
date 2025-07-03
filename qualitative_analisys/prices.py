from sqlalchemy.orm import joinedload
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db import make_session
from db.models.oferta import Oferta

engine, session = make_session()    

# Buscando todas as ofertas com preço <= 200
ofertas_filtradas = (
    session.query(Oferta)
    .filter(Oferta.preco <= 200)
    .all()
)

precos = [oferta.preco for oferta in ofertas_filtradas]

df = pd.DataFrame(precos, columns=['preco'])

plt.figure(figsize=(10, 6))
plt.hist(df['preco'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribuição de Preços das Ofertas (até R$ 200)')
plt.xlabel('Preço (R$)')
plt.ylabel('Quantidade de Ofertas')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("histograma_precos.png")
