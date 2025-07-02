from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from medextractor.med_extractor import AbsPageExtractor
from medextractor.url_extractor import AbsUrlExtractor
from playwright.sync_api import Page

class AbsExtractor(ABC):

    url_extractor_cls = AbsUrlExtractor
    page_extractor_cls = AbsPageExtractor
    base_url = ""

    def __init__(self):
        pass

    def _task(self, url):
        try:
            oferta = self.page_extractor_cls().extract(url)
            print(oferta)
        except Exception as e:
            print(f"Erro na url {url}")
            print(e)

    def extract(self):
        urls = self.url_extractor_cls(self.base_url).extract()
        with ThreadPoolExecutor(max_workers=10) as pool:
            pool.map(self._task, urls)
