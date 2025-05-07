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
    
    def get_preco(self) -> str:
        return None
    
    def get_code(self) -> str:
        return None
    
    def get(self, data: str) -> Medicamento:
        self.process(data)
        return asdict(Medicamento(self.get_nome(), self.get_preco(), self.get_code()))
