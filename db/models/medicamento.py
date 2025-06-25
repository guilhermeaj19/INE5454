from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
)

from sqlalchemy.orm import relationship
from db import Base


class Medicamento(Base):
    __tablename__ = "medicamento"

    id = Column(Integer, primary_key=True)
    registro_ms = Column(String(20), nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    marca = Column(String(120))
    categoria = Column(String(120))
    sub_categoria = Column(String(120))
    image_source = Column(Text)
    descricao = Column(Text)
    is_generico = Column(Boolean, default=False, nullable=False)
    necessita_prescricao = Column(Boolean, default=False, nullable=False)

    ofertas = relationship("Oferta", back_populates="medicamento")
