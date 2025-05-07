from dataclasses import dataclass

@dataclass
class Medicamento:
    nome: str
    url: str
    preco: float
    code: int
    marca: str
    categoria: str
    sub_categoria: str
    principios_ativos: list
    image_source: str