import time
import requests
from medextractor import AbsPageExtractor
import re

class SaoJoaoPageExtractor(AbsPageExtractor):
    def __init__(self):
        super().__init__()
        
    def process(self, data):
        self.page.goto(data, timeout=0)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)
        # self.page.wait_for_selector("a.vtex-store-components-3-x-productNameContainer", timeout=1000)
        # time.sleep(6)

    def get_nome(self):
        return self.page.locator("h1.vtex-store-components-3-x-productNameContainer").text_content(timeout=1000).strip()

    def get_preco(self):
        preco = float(self.page.locator("meta[property='product:price:amount']").get_attribute('content', timeout=1000).strip())
        return preco

    def get_code(self):
        return None
    
    def get_registro_ms(self):
        try:
            return self.page.locator('[data-specification-name="Registro MS"]').all()[-1].get_attribute("data-specification-value", timeout=1000).strip()
        except:
            return None
            
    def get_marca(self):
        try:
            return self.page.locator("meta[property='product:brand']").get_attribute('content', timeout=1000).strip()
        except:
            return None

    def get_categoria(self):
        try:
            return self.page.locator("a.vtex-breadcrumb-1-x-link--3").text_content(timeout=1000)
        except:
            return None
    
    def get_sub_categoria(self):
        try:
            return self.page.locator("a.vtex-breadcrumb-1-x-link--2").text_content(timeout=1000)
        except:
            return None
    
    def get_image_source(self):
        try:
            return self.page.locator("img.vtex-store-components-3-x-productImageTag--main").all()[0].get_attribute("src").strip()
        except:
            return None

    def get_is_generico(self):
        return "genérico" in self.get_nome().lower() or "generico" in self.get_nome().lower()
    
    def get_farmacia(self):
        return "ultrafarma"
