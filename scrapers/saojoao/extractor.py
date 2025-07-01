from abc import ABC
from medextractor import AbsExtractor
from scrapers.saojoao.page import SaoJoaoPageExtractor
from scrapers.saojoao.url import SaoJoaoUrlExtractor

class SaoJoaoExtractor(AbsExtractor):

    url_extractor_cls = SaoJoaoUrlExtractor
    page_extractor_cls = SaoJoaoPageExtractor

    def __init__(self, page, db):
        super().__init__(page, db)