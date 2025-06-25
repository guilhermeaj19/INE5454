import time
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from db.models import Farmacia, Medicamento, Oferta, PrincipioAtivo
from typing import List, Optional, Iterable
from datetime import datetime
from decimal import Decimal
from typing import Optional, Iterable
from sqlalchemy import select, update, insert
from sqlalchemy.orm import joinedload
from db import Session

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


class PrincipioAtivoRepo:
    """
    Camada de acesso a dados para a entidade PrincipioAtivo.
    Recebe uma instância de `Session` aberta no construtor
    (o mesmo padrão dos demais repositórios do projeto).
    """

    def __init__(self, db) -> None:
        self.db = db

    # ------------------------------------------------------------------
    # CRUD BÁSICO
    # ------------------------------------------------------------------
    def get(self, pa_id: int) -> Optional[PrincipioAtivo]:
        """Busca pelo ID primário."""
        return self.db.get(PrincipioAtivo, pa_id)

    def list_all(self) -> List[PrincipioAtivo]:
        """Retorna todos os princípios ativos ordenados pelo nome."""
        stmt = select(PrincipioAtivo).order_by(PrincipioAtivo.nome)
        return self.db.scalars(stmt).all()

    def add(self, pa: PrincipioAtivo, flush: bool = True) -> PrincipioAtivo:
        """Adiciona um objeto já criado à sessão."""
        self.db.add(pa)
        if flush:
            self.db.flush([pa])
        return pa

    def delete(self, pa: PrincipioAtivo) -> None:
        """Remove o objeto da base (commit é responsabilidade externa)."""
        self.db.delete(pa)

    # ------------------------------------------------------------------
    # BUSCAS POR NOME
    # ------------------------------------------------------------------
    def get_by_nome(
        self, nome: str, case_insensitive: bool = True
    ) -> Optional[PrincipioAtivo]:
        """Procura pelo campo `nome` (único)."""
        stmt = (
            select(PrincipioAtivo)
            .where(
                func.lower(PrincipioAtivo.nome) == nome.lower()
                if case_insensitive
                else PrincipioAtivo.nome == nome
            )
        )
        return self.db.scalars(stmt).one_or_none()

    # ------------------------------------------------------------------
    # GET-OR-CREATE
    # ------------------------------------------------------------------
    def get_or_create(
        self, nome: str, flush: bool = True, case_insensitive: bool = True
    ) -> PrincipioAtivo:
        """
        Retorna o registro caso exista; caso contrário cria um novo.
        Garante que o objeto resultante já tenha `id`.
        """
        pa = self.get_by_nome(nome, case_insensitive)
        if pa is None:
            pa = PrincipioAtivo(nome=nome)
            self.db.add(pa)
            if flush:
                self.db.flush([pa])
        return pa

    # ------------------------------------------------------------------
    # BULK GET-OR-CREATE
    # ------------------------------------------------------------------
    def bulk_get_or_create(
        self, nomes: Iterable[str], flush: bool = True
    ) -> List[PrincipioAtivo]:
        """
        Recebe um iterável de strings e devolve uma lista de objetos
        `PrincipioAtivo`, criando os que ainda não existirem.
        """
        if nomes == None:
            return None
        
        objs: list[PrincipioAtivo] = []
        lowered = [n.lower() for n in nomes]

        # 1) pega os que já existem
        stmt = select(PrincipioAtivo).where(func.lower(PrincipioAtivo.nome).in_(lowered))
        existentes = {
            pa.nome.lower(): pa for pa in self.db.scalars(stmt).all()
        }

        # 2) reaproveita ou cria
        for nome in nomes:
            pa = existentes.get(nome.lower())
            if pa is None:
                pa = PrincipioAtivo(nome=nome)
                self.db.add(pa)
                objs.append(pa)
            else:
                objs.append(pa)

        if flush:
            self.db.flush(objs)

        return objs


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