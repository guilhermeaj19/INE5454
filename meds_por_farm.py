from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento, Farmacia
import json

engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

count_per_farm = dict()



with Session() as db:
    medicamentos = (
        db.query(Medicamento).all()
    )

    farmacias = (
        db.query(Farmacia).all()
    )

    for f in farmacias:
        count_per_farm[f.nome] = 0

    for med in medicamentos:
        for oferta in med.ofertas:
            count_per_farm[oferta.farmacia.nome] += 1

print(f"Número de medicamentos: {len(medicamentos)}")
print(f"Medicamentos por farmácia:")
print(count_per_farm)

