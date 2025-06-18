from extractors.drogaraia.page import DrogaraiaExtractor
from extractors.drogaraia.url import DrogaraiaUrlExtractor
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()



# urlextractor = DrogaraiaUrlExtractor(page)
# print(urlextractor.get())

#Extração individual
extractor = DrogaraiaExtractor(page)
extractor.update("https://www.drogaraia.com.br/cloridrato-de-fluoxetina-20mg-teuto-generico-30-capsulas-c1.html")
input()