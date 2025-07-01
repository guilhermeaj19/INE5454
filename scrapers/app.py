from db import Session
from scrapers.drogaraia.extractor import DrogaraiaExtractor
from scrapers.farmafine.extractor import FarmafineExtractor
from scrapers.ultrafarma.extractor import UltrafarmaExtractor
from playwright.sync_api import sync_playwright


class ScraperApp:
    def __init__(self):
        self.db = Session()
        self.pw = sync_playwright().start()
        self.chrome = self.pw.chromium.launch(headless=False)
        self.page = self.chrome.new_page()
        self.extractors = [
            # DrogaraiaExtractor(self.page, self.db),
            # FarmafineExtractor(self.page, self.db),
            UltrafarmaExtractor(self.page, self.db),
        ]

    def run(self):
        for extractor in self.extractors:
            extractor.extract()

        self.db.close()
        self.page.close()
