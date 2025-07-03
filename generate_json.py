from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento
import json

engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

lista_meds = []

with Session() as db:
    medicamentos = (
        db.query(Medicamento).all()
    )

    for med in medicamentos:
        med_dict = dict([("registro_ms", med.registro_ms),
                        ("quantidade", med.quantidade),
                        ("nome", med.nome),
                        ("marca", med.marca),
                        ("categoria", med.categoria),
                        ("sub_categoria", med.sub_categoria),
                        ("image_source", med.image_source),
                        ("descricao", med.descricao),
                        ("is_generico", med.is_generico),
                        ("necessita_prescricao", med.necessita_prescricao)])
        
        med_dict["ofertas"] = dict()

        for oferta in med.ofertas:
            med_dict["ofertas"][oferta.farmacia.nome] = dict([("preco", float(oferta.preco)),
                                                            ("url", oferta.url)])
    
        lista_meds.append(med_dict)

with open("medicamentos.json", "w", encoding="utf-8") as arquivo:
    json.dump(lista_meds, arquivo, indent=2, ensure_ascii=False)
