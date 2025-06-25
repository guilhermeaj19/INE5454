import time
from sqlalchemy import func, select
from db.models import PrincipioAtivo
from typing import List, Optional, Iterable
from typing import Optional, Iterable
from sqlalchemy import select

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
