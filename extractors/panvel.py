import requests
from medextractor.helpers import AbsMedExtractor
from bs4 import BeautifulSoup
import re


class PanvelExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__(page)
        # self.s = requests.Session()

    def process(self, data):
        # self.url = data
        # self.html = self.s.get(data).text
        # self.soup = BeautifulSoup(self.html, "html.parser")
        # with open("test.html", "w+") as f:
        #     f.write(self.html)
        self.page.goto(data)
        self.page.wait_for_selector("span.deal-price.ng-star-inserted")

    def get_nome(self):
    #   return self.soup.find(
    #         "h1", {"class": "product-title"}
    #   ).text.strip()
        return self.page.locator("h1.product-title").text_content().strip()
    
    def get_url(self):
        return self.url

    def get_preco(self):
        original = self.page.locator("span.deal-price.ng-star-inserted").text_content().strip()
        return float(re.sub(r"R\$ (\d+),(\d{2})", "\\1.\\2", original))

    def get_code(self):
        # return int(self.soup.find(
        #     "span", {"class": "product-detail__sku"}
        # ).text.split()[1])
        return int(self.page.locator("span.product-detail__sku").text_content().split()[-1])
    
    def get_marca(self):
        """
            Diferente das outras, essa não tem um lugar indicando a marca sozinha.
            Buscar outra forma de coletar
        """
        # return self.soup.find(
        #             "span", {"class": "vtex-store-components-3-x-productBrandName"}
        #         ).text.strip()
        return None

    def get_categoria(self):
        # container = self.soup.find_all(
        #             "div", {"class": "container-categories ng-star-inserted"})[1]
        # return container.find(
        #     "a", {"class": "title"}
        # ).text.strip()
        return self.page.locator("div.container-categories.ng-star-inserted a.title").all()[1].text_content().strip()
    
    def get_sub_categoria(self):
        # container = self.soup.find_all(
        #             "div", {"class": "container-categories ng-star-inserted"})
        
        # if len(container) >= 3:
        #     return container[2].find("a", {"class": "title"}).text.strip()
        # else: 
        #     return "Não possui"
        try:
            return self.page.locator("div.container-categories.ng-star-inserted a.title").all()[2].text_content().strip()
        except:
            return "Não possui"
    
    def get_principios_ativos(self):
        #Pegar por requisição
        pass
    
    def get_image_source(self):
        # return self.soup.find(
        #             "img", {"class": "img-desktop"}
        #         )['src'].strip()
        return self.page.locator("img.img-desktop").get_attribute('src').strip()

    def get_is_generico(self):
        return "generico" in self.get_nome().lower()

