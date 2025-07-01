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
    registro_ms = Column(String(20), nullable=False)
    quantidade = Column(Integer)
    nome = Column(String(255), nullable=False)
    marca = Column(String(120))
    categoria = Column(String(120))
    sub_categoria = Column(String(120))
    image_source = Column(Text)
    descricao = Column(Text)
    is_generico = Column(Boolean, default=False, nullable=False)
    necessita_prescricao = Column(Boolean, default=False, nullable=False)

    ofertas = relationship("Oferta", back_populates="medicamento")

    def __repr__(self) -> str:
        return (
            f"<Medicamento("
            f"id={self.id!r}, "
            f"registro_ms={self.registro_ms!r}, "
            f"nome={self.nome!r}, "
            f"marca={self.marca!r}, "
            f"quantidade={self.quantidade!r}, "
            f"is_generico={self.is_generico}, "
            f"necessita_prescricao={self.necessita_prescricao}"
            f")>"
        )
