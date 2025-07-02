from db import init_db, make_session
from scrapers.drogaraia.extractor import DrogaraiaExtractor
from scrapers.farmafine.extractor import FarmafineExtractor
from scrapers.ultrafarma.extractor import UltrafarmaExtractor
from scrapers.saojoao.extractor import SaoJoaoExtractor

class ScraperApp:
    def __init__(self):
        engine, Session = make_session()
        init_db(engine)

        self.extractors = [
            # DrogaraiaExtractor(),
            # FarmafineExtractor(),
            UltrafarmaExtractor(),
            SaoJoaoExtractor()
        ]

    def run(self):
        for extractor in self.extractors:
            extractor.extract()

