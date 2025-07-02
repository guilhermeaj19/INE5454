from medextractor import AbsUrlExtractor
import json

class DrogaraiaUrlExtractor(AbsUrlExtractor):

    def __init__(self, url=None):
        super().__init__(url if url else "https://www.drogaraia.com.br/medicamentos/remedios.html")

    def process(self, data = None):
        self.page.goto(data if data else "", timeout=0)
        self.page.wait_for_selector("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy")

    def setup(self):
        self.page.goto(self.url if self.url else "", timeout=0)
        self.page.wait_for_selector("a.Paginationstyles__Link-sc-1am2zyy-3")
        self.limit = int(self.page.locator("a.Paginationstyles__Link-sc-1am2zyy-3").all()[-2].text_content())

    def get_next_url(self):
        self.page_it += 1
        return f"https://www.drogaraia.com.br/medicamentos/remedios.html?page={self.page_it}"

    #TODO: arrumar a inserção no json para se tornar um json único (ou um txt) e não um jsonl
    def get_urls(self):
        self.number_of_pages = int(self.page.locator("a.Paginationstyles__Link-sc-1am2zyy-3.elEkTT").all()[-2].text_content())
        urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
        urls = [url.get_attribute("href") for url in urls_element]
        return urls
