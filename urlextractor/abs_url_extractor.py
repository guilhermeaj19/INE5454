from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright, Page

class AbsUrlExtractor(ABC):
    def __init__(self, page: Page):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_urls(self) -> list[str]:
        return None
    
    def get_url(self) -> str:
        return self.url
    
    def get(self, data):
        self.process(data)
        self.url = data
        return self.get_urls()
    