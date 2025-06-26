from medextractor import AbsUrlExtractor
import json

class DrogaraiaUrlExtractor(AbsUrlExtractor):

    def __init__(self, page, url=None):
        super().__init__(page, url if url else "https://www.drogaraia.com.br/medicamentos/remedios.html", limit=4)

    def process(self, data = None):
        self.page.goto(data if data else "")
        self.page.wait_for_selector("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy")

    def get_next_url(self):
        self.page_it += 1
        return f"https://www.drogaraia.com.br/medicamentos/remedios.html?page={self.page_it}"

    #TODO: arrumar a inserção no json para se tornar um json único (ou um txt) e não um jsonl
    def get_urls(self):
        self.number_of_pages = int(self.page.locator("a.Paginationstyles__Link-sc-1am2zyy-3.elEkTT").all()[-2].text_content())
        urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
        urls = [url.get_attribute("href") for url in urls_element]
        return urls
