from sqlalchemy.orm import Session
from db.models import Medicamento

class MedicamentoRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_registro(self, registro_ms: str) -> Medicamento | None:
        return (self.db.query(Medicamento)
                    .filter_by(registro_ms=registro_ms)
                    .one_or_none())

    def add(self, med: Medicamento) -> None:
        self.db.add(med)

