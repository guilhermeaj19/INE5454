from decimal import Decimal
from db import make_session                     # cria engine, Session e metadata [9]
from db.models.farmacia import Farmacia
from db.models.medicamento import Medicamento
from db.models.oferta import Oferta
from db.utils import upsert_medicamento_oferta   # função criada anteriormente
from sqlalchemy import func, distinct, select
from db.models.medicamento import Medicamento
from db.models.oferta import Oferta
                                        # usa MedicamentoRepo[6], FarmaciaRepo[8] e OfertaRepo[7]

# 1. Garante que as tabelas existam (executar uma única vez no início do app)
engine, db = make_session()                                         # [9]
def list_meds_sold_in_multiple_farmacias(db) -> list[Medicamento]:
    return (
        db.query(Medicamento)
        .join(Medicamento.ofertas)                # medicamento → oferta
        .group_by(Medicamento.id)
        .having(func.count(distinct(Oferta.farmacia_id)) >= 2)
        .all()
    )

# 2. Abre transação
print(len(list_meds_sold_in_multiple_farmacias(db)))
stmt = (
    select(Oferta)                 # o que queremos retornar
    .join(Oferta.farmacia)         # junta com a tabela Farmacia via relacionamento
    .where(Farmacia.nome == "farmafine")  # filtra pelo nome da farmácia
)

# ofertas_farmafine = db.scalars(stmt).all()
# print(ofertas_farmafine)
    # 3. Insere ou atualiza uma oferta
    # oferta = upsert_medicamento_oferta(
    #     db,
    #     registro_ms="1234567890124",
    #     nome="Dipirona Monoidratada 500 mg",
    #     marca="Genfar",
    #     quantidade=30,
    #     categoria="Analgésico",
    #     sub_categoria="Dor e Febre",
    #     image_source="https://exemplo.com/dipirona.jpg",
    #     descricao="Analgésico e antipirético",
    #     is_generico=True,
    #     necessita_prescricao=False,
    #     farmacia_nome="farmafine",
    #     preco=Decimal("7.85"),
    #     url="https://drogariacentral.com.br/dipirona-500mg",
    # )
    # db.add(oferta)
    # 4. Visualização amigável graças ao __repr__ implementado
    # print(db.query(Oferta).all())
    
    # Saída esperada:
    # <Oferta id=1 medicamento='Dipirona Monoidratada 500 mg' farmacia='Drogaria Central' preco=7.89>
