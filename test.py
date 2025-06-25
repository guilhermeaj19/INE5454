from db.models import Medicamento, Oferta
from scrapers.drogaraia.extractor import DrogaraiaExtractor
from playwright.sync_api import sync_playwright
from db import Session, init_db

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

# urlextractor = FarmafineUrlExtractor(page)
# print(urlextractor.get())
init_db()

with Session() as db:  # db é um Session real
    # extractor = DrogaraiaExtractor(page=page, db=db)
    # extractor.extract(
    #     "https://www.drogaraia.com.br/rosuvastatina-calcica-20mg-legrand-genericos-30-comprimidos.html"
    # )
    # faz tudo usando a mesma sessão
    # db.commit()

    extractor = DrogaraiaExtractor(page, db)
    extractor.extract()
    for o in (
        db.query(Oferta)
        .join(Oferta.medicamento)
        .filter(Medicamento.registro_ms == "1677304630091")
        .all()
    ):
        print(
            f"{o.id} | {o.medicamento.nome} | {o.farmacia.nome} | R$ {float(o.preco):.2f} | {o.medicamento.registro_ms}"
        )

    for m in db.query(Medicamento).all():
        print(m.registro_ms)
