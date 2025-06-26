from db.models import Medicamento, Oferta
from scrapers.drogaraia.extractor import DrogaraiaExtractor
from playwright.sync_api import sync_playwright
from db import Session, init_db

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

init_db()

with Session() as db:  # db é um Session real
    extractor = DrogaraiaExtractor(page, db)
    extractor.extract()
    for o in db.query(Oferta).all():
        print(o)
