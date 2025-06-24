from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from db.models import Medicamento
from playwright.sync_api import Page


class AbsUrlExtractor(ABC):
    def __init__(self, page: Page, url = None, path = None, limit = None, page_it = None):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.url = url
        self.path = path if path else None

        #120 Páginas se limite não for definido
        self.limit = limit
        self.page_it = page_it if page_it else 1

    def setup(self, data):
        '''Operação realizada no primeiro getter'''

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
    
    def get_new(self):
        data_new = self.get()

        with open(self.path, "r") as f:
            data = set(json.load(f))

        with open(self.path, "w") as f:
            json.dump(data_new.union(data), f)

        return data_new.difference(data)
        
    def get(self):
        url_set = set()
        self.setup()
        for _ in range(self.limit):
            self.process(self.url)
            data = self.get_urls()
            self.url = self.get_next_url()
            url_set.update(data)
        
        return url_set


class AbsMedExtractor(ABC):
    def __init__(self, page: Page, manager = None):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page

        if not manager:
            self.manager.load()

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
    
    def get(self, data: str) -> Medicamento:
        self.process(data)
        self.url = data
        med = Medicamento(nome=self.get_nome(), 
                                  registro_ms=self.get_registro_ms(),
                                  marca=self.get_marca(), 
                                  categoria=self.get_categoria(), 
                                  sub_categoria=self.get_sub_categoria(),
                                  principios=self.get_principios_ativos(),
                                  image_source=self.get_image_source(),
                                  is_generico=self.get_is_generico(), 
                                  necessita_prescricao=self.get_necessita_prescricao())
        return med
