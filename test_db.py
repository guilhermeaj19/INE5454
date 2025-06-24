from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    Text,
    DateTime,
    ForeignKey,
    func,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from db.models import Base, PrincipioAtivo, Farmacia, Medicamento, Oferta

engine = create_engine("sqlite:///pharma.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, future=True)

with Session() as db:
    pa = PrincipioAtivo(nome="Dipirona")
    drog = Farmacia(nome="Drogasil")
    med = Medicamento(
        registro_ms="1234567890123",
        nome="Dipirona Monoidratada 500 mg Comprimidos",
        marca="Genérico",
        categoria="Analgésico / Antitérmico",
        sub_categoria="Dipirona",
        image_source="https://exemplo.com/dipirona.jpg",
        is_generico=True,
        necessita_prescricao=False,
        principios=[pa],
    )
    oferta = Oferta(
        medicamento=med,
        farmacia=drog,
        url="https://www.drogasil.com.br/dipirona-500mg.html",
        preco=12.90,
    )
    db.add_all([med, oferta])
    db.commit()
