from abc import ABC
from medextractor import AbsExtractor
from scrapers.drogaraia.page import DrogaraiaPageExtractor
from scrapers.drogaraia.url import DrogaraiaUrlExtractor

class DrogaraiaExtractor(AbsExtractor):

    url_extractor_cls = DrogaraiaUrlExtractor
    page_extractor_cls = DrogaraiaPageExtractor

    def __init__(self):
        super().__init__()