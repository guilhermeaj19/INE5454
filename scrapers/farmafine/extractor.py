from abc import ABC
from medextractor import AbsExtractor
from scrapers.farmafine.page import FarmafinePageExtractor
from scrapers.farmafine.url import FarmafineUrlExtractor

class FarmafineExtractor(AbsExtractor):

    url_extractor_cls = FarmafineUrlExtractor
    page_extractor_cls = FarmafinePageExtractor

    def __init__(self, page, db):
        super().__init__(page, db)