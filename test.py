from db.models import Oferta
from db.repository import FarmaciaRepo, MedicamentoRepo, OfertaRepo, PrincipioAtivoRepo
from scrapers.drogaraia.page import DrogaraiaExtractor
from scrapers.drogaraia.url import DrogaraiaUrlExtractor
from scrapers.ultrafarma.url import UltrafarmaUrlExtractor
from scrapers.ultrafarma.page import UltrafarmaExtractor
from scrapers.farmafine.url import FarmafineUrlExtractor
from playwright.sync_api import sync_playwright
from db import Session, init_db
pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

# urlextractor = FarmafineUrlExtractor(page)
# print(urlextractor.get())
init_db()

with Session() as db:               # db é um Session real
    med_repo    = MedicamentoRepo(db)
    oferta_repo = OfertaRepo(db)
    farma_repo  = FarmaciaRepo(db)
    principio_ativo_repo = PrincipioAtivoRepo(db)

    extractor = UltrafarmaExtractor(
        page=page,
        medicamento_repo=med_repo,
        oferta_repo=oferta_repo,
        farmacia_repo=farma_repo,
        principio_ativo_repo=principio_ativo_repo
    )
    extractor.extract("https://www.ultrafarma.com.br/rosuvastatina-20-mg-com-30-comprimidos-legrand-generico")
               # faz tudo usando a mesma sessão
    db.commit()  
    for o in db.query(Oferta).all():
        print(f"{o.id} | {o.medicamento.nome} | {o.farmacia.nome} | R$ {float(o.preco):.2f}")