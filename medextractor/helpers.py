from abc import ABC, abstractmethod
from dataclasses import asdict
from medextractor.entities import Medicamento

class AbsMedExtractor(ABC):

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_nome(self) -> str:
        return None
    
    def get_url(self) -> str:
        return None
    
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
    
    def get(self, data: str) -> Medicamento:
        self.process(data)
        return asdict(Medicamento(self.get_nome(), 
                                  self.get_url(),
                                  self.get_preco(), 
                                  self.get_code(), 
                                  self.get_marca(), 
                                  self.get_categoria(), 
                                  self.get_sub_categoria(),
                                  self.get_principios_ativos(),
                                  self.get_image_source()))
