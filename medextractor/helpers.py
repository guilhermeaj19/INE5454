from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from db.models import Medicamento, PrincipioAtivo
from playwright.sync_api import Page
import re

from db.repository import FarmaciaRepo, MedicamentoRepo, OfertaRepo, PrincipioAtivoRepo


class AbsUrlExtractor(ABC):
    def __init__(self, page: Page, url=None, path=None, limit=None, page_it=None):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.url = url
        self.path = path if path else None

        # 120 Páginas se limite não for definido
        self.limit = limit
        self.page_it = page_it if page_it else 1

    def setup(self, data):
        """Operação realizada no primeiro getter"""

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_urls(self) -> set:
        return None

    def get_next_url(self) -> str:
        pass

    def get_url(self) -> str:
        return self.url

    def extract(self):
        url_set = set()
        self.setup()
        for _ in range(self.limit):
            self.process(self.url)
            data = self.get_urls()
            self.url = self.get_next_url()
            url_set.update(data)

        return url_set


class AbsMedExtractor(ABC):
    def __init__(
        self,
        page: Page,
        medicamento_repo: MedicamentoRepo = None,
        oferta_repo: OfertaRepo = None,
        farmacia_repo: FarmaciaRepo = None,
        principio_ativo_repo: PrincipioAtivoRepo = None,
    ):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.medicamento_repo = (
            medicamento_repo if medicamento_repo else MedicamentoRepo()
        )
        self.oferta_repo = oferta_repo if oferta_repo else OfertaRepo()
        self.farmacia_repo = farmacia_repo if farmacia_repo else FarmaciaRepo()
        self.principio_ativo_repo = (
            principio_ativo_repo if principio_ativo_repo else PrincipioAtivoRepo()
        )

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_nome(self) -> str:
        return None

    def get_url(self) -> str:
        return self.url

    def get_preco(self) -> str:
        return None

    def get_code(self) -> int:
        return None

    def get_registro_ms(self) -> int:
        return None

    def get_marca(self) -> str:
        return None

    def get_categoria(self) -> str:
        return None

    def get_sub_categoria(self) -> str:
        return None

    def get_principios_ativos(self) -> list:
        return None

    def get_image_source(self) -> str:
        return None

    def get_is_generico(self) -> bool:
        return None

    def get_necessita_prescricao(self) -> bool:
        return None

    def get_farmacia(self):
        return None

    def update(self, data: str):
        med = self.get(data)
        self.manager.update(med)

    def validate(self, med: Medicamento):
        pattern = re.compile(r"\bkit\b|\bcaixas\b", re.IGNORECASE)

        # Verifica se nome contêm "kit" ou "caixas", indicando plural
        if pattern.search(med.nome):
            return False

        if not med.registro_ms:
            return False

        return True

        # medextractor/helpers.py
    # helpers.py
    def extract(self, data: str):
        med = self.get_med(data)        # cria instância temporária
        principios = self.principio_ativo_repo.bulk_get_or_create(
            [p.nome for p in med.principios]
        )

        with self.medicamento_repo.db.no_autoflush:
            db_med = self.medicamento_repo.get_by_registro(med.registro_ms)

        if db_med is None:
            # ainda não existe → adicionar e então vincular princípios
            self.medicamento_repo.add(med)
            med.principios = principios
            self.medicamento_repo.db.flush([med])
            db_med = med
        else:
            # já existe → apenas atualizar a relação
            db_med.principios = principios

        farma = self.farmacia_repo.get_or_create(self.get_farmacia())
        self.oferta_repo.upsert(db_med, farma, self.url, self.get_preco())




    def get_med(self, data: str) -> Medicamento:
        self.process(data)
        self.url = data

        principios_ativos = [
            PrincipioAtivo(nome=n) for n in self.get_principios_ativos() or []
        ]

        med = Medicamento(
            nome=self.get_nome(),
            registro_ms=self.get_registro_ms(),
            marca=self.get_marca(),
            categoria=self.get_categoria(),
            sub_categoria=self.get_sub_categoria(),
            image_source=self.get_image_source(),
            is_generico=self.get_is_generico(),
            necessita_prescricao=self.get_necessita_prescricao(),
            principios=principios_ativos,
        )

        return med
