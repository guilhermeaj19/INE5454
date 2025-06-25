from sqlalchemy import (
    Column, Integer, Numeric, Text,
    DateTime, ForeignKey,UniqueConstraint
)
from sqlalchemy.orm import relationship
from db import Base


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

    medicamento = relationship("Medicamento", back_populates="ofertas")
    farmacia    = relationship("Farmacia",    back_populates="ofertas")
