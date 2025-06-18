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
    
    def get_new(self):
        data_new = self.get()

        with open(self.path, "r") as f:
            data = set(json.load(f))

        with open(self.path, "w") as f:
            json.dump(data_new.union(data), f)

        return data_new.difference(data)
        
    def get(self):
        url_set = set()
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
        self.manager = manager if manager else DataManager()

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
        med = Medicamento(self.get_nome(), 
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
                                  self.get_necessita_prescricao(),
                                  self.get_farmacia())
        return med

class DataManager:
    def __init__(self, d: dict = None):
        self.d = d

    def update(self, m: Medicamento):
        
        if m.registro_ms not in self.d:
            self.d[m.registro_ms] = asdict(m)
            self.d[m.registro_ms].pop("url", None)
            self.d[m.registro_ms].pop("farmacia", None)
            self.d[m.registro_ms].pop("preco", None)
            self.d[m.registro_ms]["farmacias"] = {}
        
        self.d[m.registro_ms]["farmacias"][m.farmacia] = {"preco": m.preco, "url": m.url}
        self.save()

    def load(self, path = None):
        path = path if path else "extracted_data/data.json"
        with open(path, "r") as f:
            self.d = json.load(f)

    def get_urls_farmacia(self, farmacia):
        for key in self.d:
            if farmacia in self.d[key]["farmacias"]:
                return self.d[key]["farmacias"][farmacia]["url"]

    def save(self, path = None):
        path = path if path else "extracted_data/data.json"
        with open(path, "w") as f:
            json.dump(self.d, f)
