from db import Session
from scrapers.drogaraia.extractor import DrogaraiaExtractor
from scrapers.farmafine.extractor import FarmafineExtractor
from scrapers.ultrafarma.extractor import UltrafarmaExtractor
from scrapers.saojoao.extractor import SaoJoaoExtractor
from playwright.sync_api import sync_playwright

class ScraperApp:
    def __init__(self):
        self.extractors = [
            # DrogaraiaExtractor(),
            # FarmafineExtractor(),
            # UltrafarmaExtractor(),
            SaoJoaoExtractor()
        ]

    def run(self):
        for extractor in self.extractors:
            extractor.extract()

        self.db.close()
        self.page.close()
