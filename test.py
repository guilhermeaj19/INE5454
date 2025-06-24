from scrapers.drogaraia.page import DrogaraiaExtractor
from scrapers.drogaraia.url import DrogaraiaUrlExtractor
from scrapers.ultrafarma.url import UltrafarmaUrlExtractor
from scrapers.ultrafarma.page import UltrafarmaExtractor
from scrapers.farmafine.url import FarmafineUrlExtractor
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

urlextractor = FarmafineUrlExtractor(page)
print(urlextractor.get())

# #Extração individual
# extractor = UltrafarmaExtractor(page)
# extractor.update("https://www.ultrafarma.com.br/rosuvastatina-20-mg-com-30-comprimidos-legrand-generico")
# input()