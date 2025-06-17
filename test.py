from extractors.drogaraia.page import DrogaraiaExtractor
from extractors.drogaraia.url import DrogaraiaUrlExtractor
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

urlextractor = DrogaraiaUrlExtractor(page)
print(urlextractor.get())

#Extração individual
extractor = DrogaraiaExtractor(page)
data = extractor.get("https://www.drogasil.com.br/tadalafila-20mg-neo-quimica-generico-1-comprimidos-revestidos.html?origin=search")
print(data)