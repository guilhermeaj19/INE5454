from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from medextractor.entities import Medicamento
from playwright.sync_api import Page


class AbsUrlExtractor(ABC):
    def __init__(self, page: Page, url = None, path = None, limit = None, page_it = None):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.url = url
        self.path = path if path else None

        #120 Páginas se limite não for definido
        self.limit = limit if limit else 120
        self.page_it = page_it if page_it else 1

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_urls(self) -> list[str]:
        return None
    
    def get_next_url(self) -> str:
        pass
    
    def get_url(self) -> str:
        return self.url
    
    def get(self):
        url_set = set()
        for _ in range(self.limit):
            self.process(self.url)
            data = self.get_urls()
            self.url = self.get_next_url()
            url_set.update(data)

        with open(self.path + "/all.json", "wr+") as f:
            data = set(json.load(f))
            data_new = data.copy()
            data_new.update(url_set)
            json.dump(list(url_set), f)

        with open(self.path + "/new.json", "w+") as f:
            #Intersecção de estados
            new = url_set.difference(data)
            json.dump(list(new), f)


class AbsMedExtractor(ABC):
    def __init__(self, page: Page):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page

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
    
    def get(self, data: str) -> Medicamento:
        self.process(data)
        self.url = data
        med = asdict(Medicamento(self.get_nome(), 
                                  self.get_url(),
                                  self.get_preco(), 
                                  self.get_code(), 
                                  self.get_registro_ms(),
                                  self.get_marca(), 
                                  self.get_categoria(), 
                                  self.get_sub_categoria(),
                                  self.get_principios_ativos(),
                                  self.get_image_source(),
                                  self.get_is_generico(), 
                                  self.get_necessita_prescricao()))
        return med
