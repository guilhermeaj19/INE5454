from db.models.oferta import Oferta
from scrapers.drogaraia.page import DrogaraiaPageExtractor
from scrapers.farmafine.page import FarmafinePageExtractor
from scrapers.ultrafarma.page import UltrafarmaPageExtractor
from playwright.sync_api import sync_playwright
from decimal import Decimal
from db import init_db, Session                     # cria engine, Session e metadata [9]
from db.models.medicamento import Medicamento
from db.utils import upsert_medicamento_oferta   # função criada anteriormente
                                                    # usa MedicamentoRepo[6], FarmaciaRepo[8] e OfertaRepo[7]

# 1. Garante que as tabelas existam (executar uma única vez no início do app)
init_db()                                           # [9]
db = Session()
pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()
# 2. Abre transação
with Session() as db:
    # drogaraia = DrogaraiaPageExtractor(page, db)
    # med = drogaraia.extract("https://www.drogaraia.com.br/tadalafila-5mg-eurofarma-generico-30-comprimidos-revestidos.html?origin=search")
    # print(med)
    farmafine = FarmafinePageExtractor(page, db)
    med = farmafine.extract("https://farmafine.com.br/products/de-tadalafila-diario-eurofarma-5mg-com-30-comprimidos-de?_pos=3&_sid=2f1f4b487&_ss=r")
    # ultrafarma = UltrafarmaPageExtractor(page,db)
    # med = ultrafarma.extract("https://www.ultrafarma.com.br/tadalafila-5-mg-com-30-comprimidos-eurofarma-generico")
    print(med)
    print(db.query(Medicamento).all())
