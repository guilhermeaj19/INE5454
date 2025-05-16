import requests
from medextractor.helpers import AbsMedExtractor
from bs4 import BeautifulSoup


class PanvelExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__()
        self.s = requests.Session()

    def process(self, data):
        self.url = data
        self.html = self.s.get(data).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        with open("test.html", "w+") as f:
            f.write(self.html)

    def get_nome(self):
        return self.soup.find(
            "h1", {"class": "product-title"}
        ).text.strip()
    
    def get_url(self):
        return self.url

    def get_preco(self):
        #Pegar por requisição
        pass

    def get_code(self):
        return int(self.soup.find(
            "span", {"class": "product-detail__sku"}
        ).text.split()[1])
    
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
        """
            Aparentemente, este atributo não está presente no html estático
            Necessita coletar via resquisição
        """
        # container = self.soup.find_all(
        #             "div", {"class": "container-categories ng-star-inserted"})[1]
        # return container.find(
        #     "a", {"class": "title"}
        # ).text.strip()
    
    def get_sub_categoria(self):
        """
            Aparentemente, este atributo não está presente no html estático
            Necessita coletar via resquisição
        """
        # container = self.soup.find_all(
        #             "div", {"class": "container-categories ng-star-inserted"})
        
        # if len(container) >= 3:
        #     return container[2].find("a", {"class": "title"}).text.strip()
        # else: 
        #     return "Não possui"
    
    def get_principios_ativos(self):
        #Pegar por requisição
        pass
    
    def get_image_source(self):
        return self.soup.find(
                    "img", {"class": "img-desktop"}
                )['src'].strip()


