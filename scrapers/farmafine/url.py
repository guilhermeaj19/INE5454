from medextractor import AbsUrlExtractor

class FarmafineUrlExtractor(AbsUrlExtractor):
    def __init__(self, url=None):
        super().__init__(url if url else "https://farmafine.com.br/collections/medicamentos?page=1")

    def setup(self):
        self.page.goto(self.url if self.url else "", timeout=0)
        self.page.wait_for_selector("a.pagination__nav-item")
        self.limit = int(self.page.locator("a.pagination__nav-item").all()[-1].text_content())

    def process(self, data = None):
        if data is not None:
            self.page.goto(data if data else "", timeout=0)
        self.page.wait_for_selector("a.product-item__image-wrapper")
    
    def get_next_url(self):
        self.page_it += 1
        return f"https://farmafine.com.br/collections/medicamentos?page={self.page_it}"

    #TODO: arrumar a inserção no json para se tornar um json único (ou um txt) e não um jsonl
    def get_urls(self):
        urls_element = self.page.locator("a.product-item__image-wrapper ").all()
        urls = set(url.get_attribute("href") for url in urls_element)
        return [f"https://farmafine.com.br{url}" for url in urls]
        # with open("urlextractor/drogaria.jsonl", 'w', encoding="utf-8") as file:
        #     file.write(str(json.dumps({1: [url.get_attribute('href') for url in urls_element]}, indent=4)))
            
        #     for i in range(2, 192):
        #         self.process(self.url + str(i))
        #         urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
        #         file.write(str(json.dumps({i: [url.get_attribute('href') for url in urls_element]}, indent=4))+'\n')