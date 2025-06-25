from abc import ABC
from medextractor.med_extractor import AbsMedExtractor
from medextractor.url_extractor import AbsUrlExtractor
from playwright.sync_api import Page

class AbsExtractor(ABC):

    url_extractor_cls = AbsUrlExtractor
    med_extractor_cls = AbsMedExtractor
    base_url = ""

    def __init__(self, page: Page):
        self.url_extractor = self.url_extractor_cls(page)
        self.med_extractor = self.med_extractor_cls(page)

    def extract():
        pass