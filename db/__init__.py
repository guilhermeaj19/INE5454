from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URL = "sqlite:///{}".format(Path(__file__).parent.parent / "pharma.db")

# engine = create_engine(DB_URL, echo=False)

# Session = sessionmaker(bind=engine)

def init_db(engine) -> None:
    import db.models               # carrega classes no metadata
    Base.metadata.create_all(bind=engine)

Base = declarative_base()

def make_session():
    engine = create_engine(DB_URL, pool_pre_ping=True)  # new engine per proc
    Session = scoped_session(sessionmaker(bind=engine))
    return engine, Session