from sqlalchemy import (
    Column, Integer, String, 
)
from sqlalchemy.orm import relationship
from db import Base

class Farmacia(Base):
    __tablename__ = "farmacia"
    id   = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False, unique=True)
    ofertas = relationship("Oferta", back_populates="farmacia")