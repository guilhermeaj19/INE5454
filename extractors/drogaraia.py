import requests
from medextractor.helpers import AbsMedExtractor
import re

class DrogaraiaExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)
        self.page.wait_for_selector("span.ProductPricestyles__Price-i0kwh2-5.kbMdBR", state="hidden")

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)

    def get_nome(self):
        return self.page.locator("h1.Titlestyles__TitleStyles-sc-1deip5w-0.kGDgiE").text_content().strip()

    def get_preco(self):
        text = self.page.locator("span.ProductPricestyles__Price-i0kwh2-5.kbMdBR").last.text_content().strip()
        return float(re.sub(r"Por  R\$ (\d+),(\d{2})", r"\1.\2", text))

    def get_code(self):
        try:
            return int(self.page.locator("//span[contains(@class, 'RaiaProductDescriptionstyles__Title-sc') and text()='SKU']/following-sibling::span/div").text_content().strip())
        except:
            return None
    
    def get_registro_ms(self):
        try:
            return int(self.page.locator("//span[contains(@class, 'RaiaProductDescriptionstyles__Title-sc') and text()='MS']/following-sibling::span/div").text_content().strip())
        except:
            return None
            
    def get_marca(self):
        try:
            return self.page.locator("//span[contains(@class, 'RaiaProductDescriptionstyles__Title-sc') and text()='Marca']/following-sibling::span/span/a").text_content().strip()
        except:
            return None

    def get_categoria(self):
        try:
            return self.page.locator("li.Breadcrumbsstyles__Item-fir7a9-1.kKFsBt a").all()[1].text_content()
        except:
            return None
    
    def get_sub_categoria(self):
        try:
            return self.page.locator("li.Breadcrumbsstyles__Item-fir7a9-1.kKFsBt a").all()[2].text_content()
        except:
            return None
    
    def get_principios_ativos(self):
        try:
            return self.page.locator("//span[contains(@class, 'RaiaProductDescriptionstyles__Title-sc') and text()='Princípio Ativo Novo']/following-sibling::span/span/a").text_content().strip().split(",")
        except:
            return None
    
    def get_image_source(self):
        try:
            return self.page.locator("img.swiper-lazy.small-image[src][style*='width:100%;height:auto;display:block;pointer-events:none']").get_attribute('src')
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
