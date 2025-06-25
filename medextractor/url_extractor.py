from abc import ABC

from streamlit import Page


class AbsUrlExtractor(ABC):
    def __init__(self, page: Page, url=None, path=None, limit=None, page_it=None):
        # self.pw = sync_playwright().start()
        # self.chrome = self.pw.chromium.launch(headless=False)
        self.page = page
        self.url = url
        self.path = path if path else None

        # 120 Páginas se limite não for definido
        self.limit = limit
        self.page_it = page_it if page_it else 1

    def setup(self, data):
        """Operação realizada no primeiro getter"""

    def process(self, data):
        """Operação realizada antes de chamar os getters
        Pode ser utilizada para, por exemplo, retornar
        uma página antes de processar campos"""

    def get_urls(self) -> set:
        return None

    def get_next_url(self) -> str:
        pass

    def get_url(self) -> str:
        return self.url

    def extract(self):
        url_set = set()
        self.setup()
        for _ in range(self.limit):
            self.process(self.url)
            data = self.get_urls()
            self.url = self.get_next_url()
            url_set.update(data)

        return url_set