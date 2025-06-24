from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Numeric, Text,
    DateTime, ForeignKey, func, Table, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from db import Base

# Tabela associativa p/ princípios-ativos n - n
medicamento_principio_ativo = Table(
    "medicamento_principio_ativo", Base.metadata,
    Column("medicamento_id", ForeignKey("medicamento.id", ondelete="CASCADE"),
           primary_key=True),
    Column("principio_ativo_id", ForeignKey("principio_ativo.id",
           ondelete="CASCADE"), primary_key=True)
)

class Farmacia(Base):
    __tablename__ = "farmacia"
    id   = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False, unique=True)
    ofertas = relationship("Oferta", back_populates="farmacia")

class PrincipioAtivo(Base):
    __tablename__ = "principio_ativo"
    id   = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False, unique=True)
    medicamentos = relationship(
        "Medicamento", secondary=medicamento_principio_ativo,
        back_populates="principios"
    )

class Medicamento(Base):
    __tablename__ = "medicamento"

    id                   = Column(Integer, primary_key=True)
    registro_ms          = Column(String(20), nullable=False, unique=True)
    nome                 = Column(String(255), nullable=False)
    marca                = Column(String(120))
    categoria            = Column(String(120))
    sub_categoria        = Column(String(120))
    image_source         = Column(Text)
    is_generico          = Column(Boolean, default=False, nullable=False)
    necessita_prescricao = Column(Boolean, default=False, nullable=False)

    principios = relationship(
        "PrincipioAtivo", secondary=medicamento_principio_ativo,
        back_populates="medicamentos"
    )
    ofertas    = relationship("Oferta", back_populates="medicamento")

class Oferta(Base):
    __tablename__ = "oferta"
    __table_args__ = (UniqueConstraint("medicamento_id", "farmacia_id"),)

    id             = Column(Integer, primary_key=True)
    medicamento_id = Column(Integer, ForeignKey("medicamento.id",
                        ondelete="CASCADE"), nullable=False)
    farmacia_id    = Column(Integer, ForeignKey("farmacia.id",
                        ondelete="CASCADE"), nullable=False)
    url            = Column(Text, nullable=False)
    preco          = Column(Numeric(12, 2), nullable=False)
    coletado_em    = Column(DateTime, server_default=func.now(), nullable=False)

    medicamento = relationship("Medicamento", back_populates="ofertas")
    farmacia    = relationship("Farmacia",    back_populates="ofertas")
