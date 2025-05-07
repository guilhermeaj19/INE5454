import requests
from medextractor.helpers import AbsMedExtractor
from bs4 import BeautifulSoup


class CatarinenseExtractor(AbsMedExtractor):
    def __init__(self):
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
            "span", {"class": "vtex-store-components-3-x-productBrand"}
        ).text.strip()
    
    def get_url(self):
        return self.url

    def get_preco(self):
        #Pegar por requisição
        pass

    def get_code(self):
        return int(self.soup.find(
            "span", {"class": "vtex-product-identifier-0-x-product-identifier__value"}
        ).text)
    
    def get_marca(self):
        return self.soup.find(
                    "span", {"class": "vtex-store-components-3-x-productBrandName"}
                ).text.strip()

    def get_categoria(self):
        return self.soup.find(
                    "a", {"class": "vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--breadcrumb-product vtex-breadcrumb-1-x-link--2 vtex-breadcrumb-1-x-link--breadcrumb-product--2 dib pv1 link ph2 c-muted-2 hover-c-link"}
                ).text.strip()
    
    def get_sub_categoria(self):
        result = self.soup.find(
                    "a", {"class": "vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--breadcrumb-product vtex-breadcrumb-1-x-link--3 vtex-breadcrumb-1-x-link--breadcrumb-product--3 dib pv1 link ph2 c-muted-2 hover-c-link"}
                )
        
        return result.text.strip() if result else "Não possui"
    
    def get_principios_ativos(self):
        #Pegar por requisição
        pass
    
    def get_image_source(self):
        return self.soup.find(
                    "img", {"class": "vtex-store-components-3-x-productImageTag"}
                )['src'].strip()


