from urlextractor.abs_url_extractor import AbsUrlExtractor
import json

class DrogaraiaUrlExtractor(AbsUrlExtractor):

    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)
        self.page.wait_for_selector("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy")

    #TODO: arrumar a inserção no json para se tornar um json único (ou um txt) e não um jsonl
    def get_urls(self):
        self.number_of_pages = int(self.page.locator("a.Paginationstyles__Link-sc-1am2zyy-3.elEkTT").all()[-2].text_content())
        urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
        
        with open("urlextractor/drogaria.jsonl", 'w', encoding="utf-8") as file:
            file.write(str(json.dumps({1: [url.get_attribute('href') for url in urls_element]}, indent=4)))
            
            for i in range(2, 192):
                self.process(self.url + str(i))
                urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
                file.write(str(json.dumps({i: [url.get_attribute('href') for url in urls_element]}, indent=4))+'\n')