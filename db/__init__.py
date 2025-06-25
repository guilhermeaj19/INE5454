from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///{}".format(Path(__file__).parent.parent.parent / "pharma.db")

engine = create_engine(DB_URL, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()

def init_db() -> None:
    """
    Cria as tabelas somente se ainda não existirem.
    Chame em ambiente de dev; em produção use Alembic.
    """
    import db.models       # registra todas as classes no metadata
    Base.metadata.create_all(bind=engine)