import requests
from medextractor.helpers import AbsMedExtractor
import re

class UltrafarmaExtractor(AbsMedExtractor):
    def __init__(self, page, db):
        super().__init__(page, db)
        
    def process(self, data):
        self.page.goto(data)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)
        self.page.wait_for_selector("div.tab-pagination-item")

    def get_nome(self):
        return self.page.locator("h2.product-title").text_content().strip()

    def get_preco(self):
        price_pix = self.page.locator("div.product-price-pix")
        price = float(price_pix.locator("b").get_attribute("data-preco").replace(",","."))
        return price

    def get_code(self):
        reference = self.page.locator("div.product-references-rating-actions")
        return reference.locator("strong").inner_text().strip()
    
    def get_registro_ms(self):
        try:
            return self.page.locator("#attr-registroms").get_attribute("data-attr-value").strip()
        except:
            return None
            
    def get_marca(self):
        try:
            return self.page.locator("a.brand-link").text_content().strip()
        except:
            return None

    def get_categoria(self):
        try:
            nav = self.page.locator("ul.navigation-pages")
            item = nav.locator('li[itemprop="itemListElement"]').all()[1]
            span = item.locator('span[itemprop="name"]').text_content()
            return span.strip()
        except:
            return None
    
    def get_sub_categoria(self):
        try:
            nav = self.page.locator("ul.navigation-pages")
            item = nav.locator('li[itemprop="itemListElement"]').all()[2]
            span = item.locator('span[itemprop="name"]').text_content()
            return span.strip()
        except:
            return None
    
    def get_principios_ativos(self):
        try:
            principio_span = self.page.locator("#attr-principioativo")
            text = principio_span.text_content().split(":")[1]
            return [text.strip()]
        except:
            return None
    
    def get_image_source(self):
        return self.page.locator("#product-image").get_attribute("src").strip()
        
    def get_is_generico(self):
        return "genérico" in self.get_nome().lower() or "generico" in self.get_nome().lower()

    def get_necessita_prescricao(self):
        return None
    
    def get_farmacia(self):
        return "ultrafarma"
