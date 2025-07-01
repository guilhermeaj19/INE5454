from decimal import Decimal
from db import init_db, Session                     # cria engine, Session e metadata [9]
from db.models.medicamento import Medicamento
from db.models.oferta import Oferta
from db.utils import upsert_medicamento_oferta   # função criada anteriormente
                                                    # usa MedicamentoRepo[6], FarmaciaRepo[8] e OfertaRepo[7]

# 1. Garante que as tabelas existam (executar uma única vez no início do app)
init_db()                                           # [9]

# 2. Abre transação
with Session() as db:
    # 3. Insere ou atualiza uma oferta
    oferta = upsert_medicamento_oferta(
        db,
        registro_ms="1234567890124",
        nome="Dipirona Monoidratada 500 mg",
        marca="Genfar",
        quantidade=30,
        categoria="Analgésico",
        sub_categoria="Dor e Febre",
        image_source="https://exemplo.com/dipirona.jpg",
        descricao="Analgésico e antipirético",
        is_generico=True,
        necessita_prescricao=False,
        farmacia_nome="farmafine",
        preco=Decimal("7.85"),
        url="https://drogariacentral.com.br/dipirona-500mg",
    )
    db.add(oferta)
    # 4. Visualização amigável graças ao __repr__ implementado
    print(db.query(Oferta).all())
    # Saída esperada:
    # <Oferta id=1 medicamento='Dipirona Monoidratada 500 mg' farmacia='Drogaria Central' preco=7.89>
