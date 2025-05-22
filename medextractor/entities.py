from dataclasses import dataclass

@dataclass
class Medicamento:
    nome: str
    url: str
    preco: float #
    code: int
    registro_ms: int
    marca: str ##
    categoria: str
    sub_categoria: str
    principios_ativos: list # ##
    image_source: str
    is_generico: bool #
    necessita_prescricao: bool #
    # necessita_receita: bool
    # descricao: str

    # avaliacao: float #
    # preco_original: float #
    # desconto_aplicado: float #