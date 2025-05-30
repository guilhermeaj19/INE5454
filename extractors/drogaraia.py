import requests
from medextractor.helpers import AbsMedExtractor
import re

class DrogaraiaExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)
        self.page.wait_for_selector("span.sc-dce0c2fc-4.hPCOGR")

    def get_nome(self):
        return eval(self.page.locator("script[type='application/ld+json']").text_content())['name']

    def get_preco(self):
        return float(self.page.locator("meta[property='product:price:amount']").get_attribute('content').strip())

    def get_code(self):
        try:
            return int(eval(self.page.locator("script[type='application/ld+json']").text_content())['sku'])
        except:
            return None
    
    def get_registro_ms(self):
        try:
            registro_ms_span = self.page.locator("span.sc-dce0c2fc-4.hPCOGR:has-text('Registro MS')")
            return int(registro_ms_span.locator("xpath=following-sibling::span").inner_text())
        except Exception as e:
            return None
            
    def get_marca(self):
        try:
            return eval(self.page.locator("script[type='application/ld+json']").text_content())['brand']['name']
        except:
            return None

    def get_categoria(self):
        try:
            return self.page.locator("a.sc-4e253ef5-0.cyULBC").all()[2].text_content()
        except:
            return None
    
    def get_sub_categoria(self):
        try:
            if self.page.locator("a.sc-4e253ef5-0.cyULBC").count() >= 4:
                return self.page.locator("a.sc-4e253ef5-0.cyULBC").all()[3].text_content()
            return None
        except:
            return None
    
    def get_principios_ativos(self):
        try:
            principio_span = self.page.locator("span.sc-dce0c2fc-4.hPCOGR:has-text('Princípio Ativo')")
            principio_ativo = principio_span.locator("xpath=following-sibling::span/a").inner_text()
            return principio_ativo.split(',')
        except:
            return None
    
    def get_image_source(self):
        try:
            return eval(self.page.locator("script[type='application/ld+json']").text_content())['image']
        except:
            return None
        
    def get_is_generico(self):
        box = "//p[contains(@style, 'border:1px solid #666')][contains(@style, 'font-size:11px')]"
        if self.page.is_visible(box, timeout=1000):
            text = self.page.locator(box).last.text_content()
            return "genérico" in text.lower()
        return False

    def get_necessita_prescricao(self):
        box = "//p[contains(@style, 'border:1px solid #666')][contains(@style, 'font-size:11px')]"
        if self.page.is_visible(box, timeout=1000):
            text = self.page.locator(box).last.text_content()
            return "prescrição" in text.lower()
        return False
