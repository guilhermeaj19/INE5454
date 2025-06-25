from abc import ABC
from db.models import Medicamento
from playwright.sync_api import Page
import re

from db.repository import FarmaciaRepo, MedicamentoRepo, OfertaRepo, PrincipioAtivoRepo

class AbsMedExtractor(ABC):
    def __init__(
        self,
        page: Page,
        db
    ):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.medicamento_repo = MedicamentoRepo(db)
        self.oferta_repo =  OfertaRepo(db)
        self.farmacia_repo = FarmaciaRepo(db)
        self.principio_ativo_repo = PrincipioAtivoRepo(db)

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

        med = self.get_med(data)
        if not self.validate(med):
            return None
    
        principios = self.principio_ativo_repo.bulk_get_or_create(self.get_principios_ativos())

        with self.medicamento_repo.db.no_autoflush:
            db_med = self.medicamento_repo.get_by_registro(med.registro_ms)

        if db_med is None:
            self.medicamento_repo.add(med)
            if principios:
                med.principios = principios
            self.medicamento_repo.db.flush([med])
            db_med = med
        else:
            db_med.principios = principios

        farma = self.farmacia_repo.get_or_create(self.get_farmacia())
        self.oferta_repo.upsert(db_med, farma, self.url, self.get_preco())


    def get_med(self, data: str) -> Medicamento:
        self.process(data)
        self.url = data

        med = Medicamento(
            nome=self.get_nome(),
            registro_ms=self.get_registro_ms(),
            marca=self.get_marca(),
            categoria=self.get_categoria(),
            sub_categoria=self.get_sub_categoria(),
            image_source=self.get_image_source(),
            is_generico=self.get_is_generico(),
            necessita_prescricao=self.get_necessita_prescricao(),
            principios=[],
        )

        return med