
from db.models.medicamento import Medicamento


class MedicamentoRepo:
    def __init__(self, db):
        self.db = db

    def get(self, med_id: int):
            return self.db.get(Medicamento, med_id)

    def get_by_registro(self, registro_ms: str) -> Medicamento | None:
        return (self.db.query(Medicamento)
                    .filter_by(registro_ms=registro_ms)
                    .one_or_none())

    def add(self, med: Medicamento) -> None:
        self.db.add(med)