from decimal import Decimal, ROUND_HALF_UP
import random

from db import init_db, Session                     # cria engine, Session e metadata [9]
from db.utils import upsert_medicamento_oferta   # função criada anteriormente
                                                    # usa MedicamentoRepo[6], FarmaciaRepo[8] e OfertaRepo[7]

# from db.models import Medicamento

# 1. Garante que as tabelas existam (executar uma única vez no início do app)
init_db()                                           # [9]

farmacias = ["Drogaria Central", "Droga Raia", "Farma Fine"]

# 2. Abre transação
with Session() as db:

    for i in range(100):

        preco_float = round(random.uniform(0, 150), 2)
        preco_decimal = Decimal(preco_float).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 3. Insere ou atualiza uma oferta
        oferta = upsert_medicamento_oferta(
            db,
            registro_ms="123456789013"+str(i),
            nome=f"{i} - Nome do Remédio",
            marca="Marca",
            quantidade=30,
            categoria="Analgésico",
            sub_categoria="Dor e Febre",
            image_source="https://assets.mypharma.com.br/StoreAdmin/product/dipirona-sodica-7899547531213",
            descricao="Analgésico e antipirético",
            is_generico=True,
            necessita_prescricao=False,
            farmacia_nome=farmacias[0],
            preco=preco_decimal,
            url="https://drogariacentral.com.br/produtos/dipironag-500mg-c30-comp-prati-7899547531213-2",
        )

        preco_float = round(random.uniform(0, 150), 2)
        preco_decimal = Decimal(preco_float).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 3. Insere ou atualiza uma oferta
        oferta = upsert_medicamento_oferta(
            db,
            registro_ms="123456789013"+str(i),
            nome=f"{i} - Nome do Remédio",
            marca="Marca",
            quantidade=30,
            categoria="Analgésico",
            sub_categoria="Dor e Febre",
            image_source="https://assets.mypharma.com.br/StoreAdmin/product/dipirona-s%C3%B3dica-7896714207551",
            descricao="Analgésico e antipirético",
            is_generico=True,
            necessita_prescricao=False,
            farmacia_nome="Farma Fine",
            preco=preco_decimal,
            url="https://farmafine.com.br/products/dipirona-1g-10-comprimidos-ems",
        )

        preco_float = round(random.uniform(0, 150), 2)
        preco_decimal = Decimal(preco_float).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 3. Insere ou atualiza uma oferta
        oferta = upsert_medicamento_oferta(
            db,
            registro_ms="123456789013"+str(i),
            nome=f"{i} - Nome do Remédio",
            marca="Marca",
            quantidade=30,
            categoria="Analgésico",
            sub_categoria="Dor e Febre",
            image_source="https://assets.mypharma.com.br/StoreAdmin/product/dipirona-sodica-7899547500363",
            descricao="Analgésico e antipirético",
            is_generico=True,
            necessita_prescricao=False,
            farmacia_nome="Droga Raia",
            preco=preco_decimal,
            url="https://www.drogaraia.com.br/neo-quimica-dipirona-gotas-500ml-gotas-sabor-abacaxi-20ml-1227961.html?origin=search",
        )

    # 4. Visualização amigável graças ao __repr__ implementado
    # print(oferta)
    # Saída esperada:
    # <Oferta id=1 medicamento='Dipirona Monoidratada 500 mg' farmacia='Drogaria Central' preco=7.89>

    # medicamentos = db.query(Medicamento).all() 
    # for med in medicamentos:
    #     print(med.nome)

    # ofertas = db.query(Medicamento).all() 
    # for of in ofertas:
    #     print(of.nome)