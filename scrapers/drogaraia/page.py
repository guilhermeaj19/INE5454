import requests
from medextractor import AbsPageExtractor
import re

class DrogaraiaPageExtractor(AbsPageExtractor):
    def __init__(self, page, db):
        super().__init__(page, db)

    def process(self, data):
        self.page.goto(data)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)
        self.page.wait_for_selector("span.sc-dce0c2fc-4.hPCOGR")

    def get_nome(self):
        return self.page.locator("h1.sc-2aea4133-1").text_content(timeout=1000)

    def get_preco(self):
        preco = float(self.page.locator("meta[property='product:price:amount']").get_attribute('content', timeout=1000).strip())
        return preco

    def get_code(self):
        try:
            return int(eval(self.page.locator("script[type='application/ld+json']").text_content(timeout=1000))['sku'])
        except:
            return None
    
    def get_registro_ms(self):
        try:
            registro_ms_span = self.page.locator("span.sc-dce0c2fc-4.hPCOGR:has-text('Registro MS')")
            return registro_ms_span.locator("xpath=following-sibling::span").inner_text(timeout=1000)
        except Exception as e:
            return None
            
    def get_marca(self):
        try:
            return eval(self.page.locator("script[type='application/ld+json']").text_content(timeout=1000))['brand']['name']
        except:
            return None

    def get_categoria(self):
        try:
            return self.page.locator("a.sc-4e253ef5-0.cyULBC").all()[2].text_content(timeout=1000)
        except:
            return None
    
    def get_sub_categoria(self):
        try:
            if self.page.locator("a.sc-4e253ef5-0.cyULBC").count() >= 4:
                return self.page.locator("a.sc-4e253ef5-0.cyULBC").all()[3].text_content(timeout=1000)
            return None
        except:
            return None
    
    def get_principios_ativos(self):
        try:
            principio_span = self.page.locator("span.sc-dce0c2fc-4.hPCOGR:has-text('Princípio Ativo')")
            principio_ativo = principio_span.locator("xpath=following-sibling::span/a").inner_text(timeout=1000)
            return principio_ativo.split(',')
        except:
            return None
    
    def get_image_source(self):
        try:
            return "https://www.drogaraia.com.br" + self.page.locator("img.main-image").get_attribute("src",timeout=1000)
        except:
            return None
        
    def get_is_generico(self):
        box = "//p[contains(@style, 'border:1px solid #666')][contains(@style, 'font-size:11px')]"
        if self.page.is_visible(box, timeout=1000):
            text = self.page.locator(box).last.text_content(timeout=1000)
            return "genérico" in text.lower()
        return False

    def get_necessita_prescricao(self):
        box = "//p[contains(@style, 'border:1px solid #666')][contains(@style, 'font-size:11px')]"
        if self.page.is_visible(box, timeout=1000):
            text = self.page.locator(box).last.text_content(timeout=1000)
            return "prescrição" in text.lower()
        return False
    
    def get_descricao(self):
        product_details = self.page.locator("#product-details")
        text_box = product_details.locator("div[data-testid='parser-script']")
        return text_box.text_content(timeout=1000)

    
    def get_farmacia(self):
        return "drogaraia"
