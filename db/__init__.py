from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DB_URL = "sqlite:///{}".format(Path(__file__).parent.parent / "pharma.db")

engine = create_engine(DB_URL, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()

def make_session():
    engine = create_engine(DB_URL, pool_pre_ping=True)  # new engine per proc
    Session = scoped_session(sessionmaker(bind=engine))
    return engine, Session

def init_db() -> None:
    """
    Cria as tabelas somente se ainda não existirem.
    Chame em ambiente de dev; em produção use Alembic.
    """
    import db.models       # registra todas as classes no metadata
    Base.metadata.create_all(bind=engine)