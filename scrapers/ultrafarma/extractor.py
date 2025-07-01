from abc import ABC
from medextractor import AbsExtractor
from scrapers.ultrafarma.page import UltrafarmaPageExtractor
from scrapers.ultrafarma.url import UltrafarmaUrlExtractor

class UltrafarmaExtractor(AbsExtractor):

    url_extractor_cls = UltrafarmaUrlExtractor
    page_extractor_cls = UltrafarmaPageExtractor

    def __init__(self, page, db):
        super().__init__(page, db)