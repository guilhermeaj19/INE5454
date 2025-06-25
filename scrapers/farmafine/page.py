from medextractor import AbsPageExtractor

class FarmafinePageExtractor(AbsPageExtractor):
    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)ultrafarma
    def get_nome(self):
        return self.page.locator("h1.product-meta__title").text_content().strip()

    def get_preco(self):
        price_all = self.page.locator("span.price--highlight").text_content()
        price = float(price_all.split("R$")[-1].strip())
        return price

    def get_code(self):
        return None
    
    def get_registro_ms(self):
        table = self.page.locator("#attr-registroms").get_attribute("data-attr-value")
        return table
            
    def get_marca(self):
        return self.page.locator('span[data-attr="principioativo"]').text_content().split(":")[-1].strip()

    def get_categoria(self):
        return "Medicamentos"
    
    def get_sub_categoria(self):
        return None
    
    def get_principios_ativos(self):
        try:
            principio_span = self.page.locator("#attr-principioativo")
            text = principio_span.text_content().split(":")[1]
            return [text.strip()]
        except:
            return None
    
    def get_image_source(self):
        return self.page.locator("img.product-gallery__image").get_attribute("data-zoom").strip()[2:]
        
    def get_is_generico(self):
        return "genérico" in self.get_nome().lower() or "generico" in self.get_nome().lower()

    def get_necessita_prescricao(self):
        return "Sem Retenção De Receita" in self.page.text_content()
    
    def get_farmacia(self):
        return "farmafine"
