import time
from medextractor import AbsUrlExtractor
import json


class SaoJoaoUrlExtractor(AbsUrlExtractor):
    def __init__(self, url=None):
        super().__init__(
            url if url else "https://www.saojoaofarmacias.com.br/medicamentos",
            limit=20,
        )

    def process(self, data=None):
        self.page.goto(data if data else "", timeout=0)

    def setup(self):
        self.page.goto(self.url if self.url else "", timeout=0)
        self.page.wait_for_selector("a.vtex-product-summary-2-x-clearLink--vitrine")

    def get_next_url(self):
        self.page_it += 1
        return f"https://www.saojoaofarmacias.com.br/medicamentos?page={self.page_it}"

    # TODO: arrumar a inserção no json para se tornar um json único (ou um txt) e não um jsonl
    def get_urls(self):
        try:
            urls_element = self.page.locator(
                "a.vtex-product-summary-2-x-clearLink--vitrine"
            ).all()
            urls = [
                "https://www.saojoaofarmacias.com.br" + url.get_attribute("href")
                for url in urls_element
            ]
            return urls
        except:
            return None
