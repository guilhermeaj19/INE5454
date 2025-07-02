from db.models.oferta import Oferta
from scrapers.drogaraia.page import DrogaraiaPageExtractor
from scrapers.drogaraia.url import DrogaraiaUrlExtractor
from scrapers.farmafine.page import FarmafinePageExtractor
from scrapers.ultrafarma.page import UltrafarmaPageExtractor
from scrapers.saojoao.page import SaoJoaoPageExtractor
from playwright.sync_api import sync_playwright
from decimal import Decimal
from db import init_db, Session                     # cria engine, Session e metadata [9]
from db.models.medicamento import Medicamento
from db.utils import upsert_medicamento_oferta   # função criada anteriormente
                                                    # usa MedicamentoRepo[6], FarmaciaRepo[8] e OfertaRepo[7]

# 1. Garante que as tabelas existam (executar uma única vez no início do app)
# 2. Abre transação

    # saojoao = SaoJoaoPageExtractor(page, db)
    # med = saojoao.extract("https://www.saojoaofarmacias.com.br/transamin-nikkho-250mg-12-comprimidos-1953/p")
    # print(med)
d = DrogaraiaUrlExtractor()
d.extract()
drogaraia1 = DrogaraiaPageExtractor()
drogaraia2 = DrogaraiaPageExtractor()
med = drogaraia1.extract("https://www.drogaraia.com.br/tadalafila-5mg-eurofarma-generico-30-comprimidos-revestidos.html?origin=search")
print(med)
med = drogaraia2.extract("https://www.drogaraia.com.br/tadalafila-5mg-eurofarma-generico-30-comprimidos-revestidos.html?origin=search")
print(med)
# farmafine = FarmafinePageExtractor(page, db)
# med = farmafine.extract("https://farmafine.com.br/products/besilato-de-anlodipino-5mg-teuto-30-comprimidos-farmafine")
# ultrafarma = UltrafarmaPageExtractor()
# med = ultrafarma.extract("https://www.ultrafarma.com.br/anlodipino-5-mg-com-30-comprimidos-teuto-generico")
# print(med)
# print(db.query(Medicamento).all())
