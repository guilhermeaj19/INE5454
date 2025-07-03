from sqlalchemy import create_engine, inspect
from pathlib import Path

def get_engine():
  db_path = format(Path(__file__).parent.parent / "pharma.db")

  engine = create_engine(f"sqlite:///{db_path}")

  return engine