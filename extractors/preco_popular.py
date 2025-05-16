import requests
from extractors.catarinense import CatarinenseExtractor
from bs4 import BeautifulSoup


class PrecoPopularExtractor(CatarinenseExtractor):
    def __init__(self, page):
        super().__init__(page)
