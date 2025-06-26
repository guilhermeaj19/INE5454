from abc import ABC
from medextractor.med_extractor import AbsPageExtractor
from medextractor.url_extractor import AbsUrlExtractor
from playwright.sync_api import Page

class AbsExtractor(ABC):

    url_extractor_cls = AbsUrlExtractor
    page_extractor_cls = AbsPageExtractor
    base_url = ""

    def __init__(self, page: Page, db):
        self.url_extractor = self.url_extractor_cls(page, self.base_url)
        self.med_extractor = self.page_extractor_cls(page, db)

    def extract(self):
        urls = self.url_extractor.extract()
        for url in urls:
            try:
                med = self.med_extractor.extract(url)
                print(med)
            except Exception as e:
                print(f"Erro na url {url}")
