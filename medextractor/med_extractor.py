from abc import ABC
from db.models import Medicamento
from playwright.sync_api import Page
from db.models.oferta import Oferta
from db.utils import upsert_medicamento_oferta
from medextractor.utils import extrai_qtd


class AbsPageExtractor(ABC):
    def __init__(
        self,
        page: Page,
        db
    ):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.db = db

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
    
    def get_quantidade(self) -> int:
        return extrai_qtd(self.get_nome())

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
    
    def get_descricao(self):
        return None

    def extract(self, data: str) -> Oferta:
        self.process(data)
        self.url = data

        med = upsert_medicamento_oferta(
            db=self.db,
            nome=self.get_nome(),
            registro_ms=self.get_registro_ms(),
            quantidade=self.get_quantidade(),
            marca=self.get_marca(),
            categoria=self.get_categoria(),
            sub_categoria=self.get_sub_categoria(),
            image_source=self.get_image_source(),
            is_generico=self.get_is_generico(),
            necessita_prescricao=self.get_necessita_prescricao(),
            descricao=self.get_descricao(),
            farmacia_nome=self.get_farmacia(),
            preco=self.get_preco(),
            url=self.url
        )

        return med
