from sqlalchemy import (
    Column, Integer, String, 
    DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from db import Base

# Tabela associativa p/ princípios-ativos n - n
medicamento_principio_ativo = Table(
    "medicamento_principio_ativo", Base.metadata,
    Column("medicamento_id", ForeignKey("medicamento.id", ondelete="CASCADE"),
           primary_key=True),
    Column("principio_ativo_id", ForeignKey("principio_ativo.id",
           ondelete="CASCADE"), primary_key=True)
)


class PrincipioAtivo(Base):
    __tablename__ = "principio_ativo"
    id   = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False, unique=True)
    medicamentos = relationship(
        "Medicamento", secondary=medicamento_principio_ativo,
        back_populates="principios"
    )