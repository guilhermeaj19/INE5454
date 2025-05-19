from abc import ABC, abstractmethod
from dataclasses import asdict
from medextractor.entities import Medicamento
from playwright.sync_api import sync_playwright, Page

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
                                  self.get_marca(), 
                                  self.get_categoria(), 
                                  self.get_sub_categoria(),
                                  self.get_principios_ativos(),
                                  self.get_image_source(),
                                  self.get_is_generico(), 
                                  self.get_necessita_prescricao()))
        return med
