from abc import ABC
from medextractor.med_extractor import AbsPageExtractor
from medextractor.url_extractor import AbsUrlExtractor
from playwright.sync_api import Page
from db import make_session
from playwright.sync_api import sync_playwright


class AbsExtractor(ABC):

    url_extractor_cls = AbsUrlExtractor
    page_extractor_cls = AbsPageExtractor
    base_url = ""

    def __init__(self):
        engine, self.db = make_session()
        self.pw = sync_playwright().start()
        self.chrome = self.pw.chromium.launch(headless=False)
        self.page = self.chrome.new_page()
        self.url_extractor = self.url_extractor_cls(self.page, self.base_url)
        self.med_extractor = self.page_extractor_cls(self.page, self.db)

    def extract(self):
        urls = self.url_extractor.extract()
        for url in urls:
            try:
                med = self.med_extractor.extract(url)
                print(med)
            except Exception as e:
                print(f"Erro na url {url}")
                print(e)
