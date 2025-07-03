from sqlalchemy import create_engine
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.models.farmacia import Farmacia
from db.models.medicamento import Medicamento
from db.models.oferta import Oferta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from engine import get_engine

engine = get_engine()

# Cria Session
Session = sessionmaker(bind=engine)
session = Session()

# JOIN e filtro
resultados = (
    session.query(Medicamento.nome, Farmacia.nome, Oferta.preco)
    .join(Oferta.medicamento)
    .join(Oferta.farmacia)
    .filter(Oferta.preco > 4000)
    .all()
)

for med_nome, farm_nome, preco in resultados:
    print(f"Medicamento: {med_nome} | Farmácia: {farm_nome} | Preço: R$ {preco:.2f}")


with engine.connect() as conn:
    query = text("""
        SELECT
          o.medicamento_id,
          m.nome AS medicamento,
          COUNT(DISTINCT o.farmacia_id) AS farmacias_distintas
        FROM
          oferta o
          JOIN medicamento m ON o.medicamento_id = m.id
        WHERE
          o.medicamento_id IN (
            SELECT medicamento_id
            FROM oferta
            WHERE preco > 4000
          )
        GROUP BY
          o.medicamento_id
        HAVING
          farmacias_distintas > 1
    """)

    result = conn.execute(query)

    for row in result:
        print(f"Medicamento: {row['medicamento']} | ID: {row['medicamento_id']} | Farmácias distintas: {row['farmacias_distintas']}")
