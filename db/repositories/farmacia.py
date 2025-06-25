from db.models.farmacia import Farmacia


class FarmaciaRepo:
    def __init__(self, db):
        self.db = db

    def get(self, farma_id: int):
            return self.db.get(Farmacia, farma_id)

    def get_by_nome(self, nome: str) -> Farmacia | None:
        return (self.db.query(Farmacia)
                    .filter_by(nome=nome)
                    .one_or_none())

    def add(self, farma: Farmacia) -> None:
        self.db.add(farma)

    def get_or_create(self, nome: str) -> Farmacia:
        farma = self.get_by_nome(nome)
        if farma is None:
            farma = Farmacia(nome=nome)
            self.db.add(farma)
            self.db.flush([farma])      # força gerar o id
        return farma