import time
from sqlalchemy import select
from db.models import Farmacia, Medicamento, Oferta
from typing import Optional
from decimal import Decimal
from typing import Optional
from sqlalchemy import select, update, insert
from sqlalchemy.orm import joinedload


class OfertaRepo:
    """Acesso à tabela oferta."""

    # -----------------------------------------------------------------
    # CONSTRUTOR
    # -----------------------------------------------------------------
    def __init__(self, db) -> None:
        self.db = db

    # -----------------------------------------------------------------
    # CRUD GENÉRICO
    # -----------------------------------------------------------------
    def get(self, oferta_id: int):
        return self.db.get(Oferta, oferta_id)

    def list_all(self):
        return self.db.scalars(select(Oferta)).all()

    def delete(self, oferta: Oferta) -> None:
        self.db.delete(oferta)

    def get_by_med_and_farm(
        self, medicamento_id: int, farmacia_id: int
    ) -> Optional[Oferta]:
        stmt = (
            select(Oferta)
            .where(
                Oferta.medicamento_id == medicamento_id,
                Oferta.farmacia_id == farmacia_id,
            )
        )
        return self.db.scalars(stmt).one_or_none()

    def list_by_medicamento(self, medicamento_id: int) -> list[Oferta]:
        return self.db.scalars(
            select(Oferta).where(Oferta.medicamento_id == medicamento_id)
        ).all()

    def list_by_registro_ms(self, registro_ms: str) -> list[Oferta]:
        """
        Todas as ofertas para um dado registro_ms, ordenadas pelo menor preço.
        """
        stmt = (
            select(Oferta)
            .join(Oferta.medicamento)
            .options(joinedload(Oferta.farmacia))
            .where(Medicamento.registro_ms == registro_ms)
            .order_by(Oferta.preco)
        )
        return self.db.scalars(stmt).all()

    def upsert(
        self,
        medicamento: Medicamento,
        farmacia: Farmacia,
        url: str,
        preco: Decimal,
    ) -> Oferta:
        """
        Se já existir oferta (medicamento,farmácia), atualiza preço e url.
        Caso contrário, cria nova linha.
        """
        oferta = self.get_by_med_and_farm(medicamento.id, farmacia.id)

        if oferta is None:
            oferta = Oferta(
                medicamento=medicamento,
                farmacia=farmacia,
                url=url,
                preco=preco,
            )
            self.db.add(oferta)
            self.db.flush([oferta])           # obtém id gerado
        else:
            oferta.url = url
            oferta.preco = preco

        return oferta

    def update_price(
        self, medicamento_id: int, farmacia_id: int, new_price: Decimal
    ) -> None:
        stmt = (
            update(Oferta)
            .where(
                Oferta.medicamento_id == medicamento_id,
                Oferta.farmacia_id == farmacia_id,
            )
            .values(preco=new_price)
        )
        self.db.execute(stmt)