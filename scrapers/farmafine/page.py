from medextractor import AbsPageExtractor

class FarmafinePageExtractor(AbsPageExtractor):
    def __init__(self, page, db):
        super().__init__(page, db)

    def process(self, data):
        self.page.goto(data)

        # html_content = self.page.content()

        # with open("result.html", "w", encoding="utf-8") as f:
        #     f.write(html_content)ultrafarma
    def get_nome(self):
        return self.page.locator("h1.product-meta__title").text_content(timeout=1000).strip()

    def get_preco(self):
        price_all = self.page.locator("span.price--highlight").all()[0].text_content(timeout=1000)
        price = float(price_all.split("R$")[-1].strip().replace(",","."))
        return price

    def get_code(self):
        return None
    
    def get_registro_ms(self):
        try:
            table = self.page.locator("#attr-registroms").get_attribute("data-attr-value",timeout=5000)
            return table
        except:
            pass
            
    def get_marca(self):
        try:
            return self.page.locator('span[data-attr="principioativo"]').text_content(timeout=1000).split(":")[-1].strip()
        except:
            pass

    def get_categoria(self):
        return "Medicamentos"
    
    def get_sub_categoria(self):
        return None
    
    def get_image_source(self):
        img = self.page.locator("img.product-gallery__image").all()
        if type(img) == list:
            img = img[0]
        
        return "https://"+ img.get_attribute("data-zoom",timeout=1000).strip()[2:]
        
    def get_is_generico(self):
        return "genérico" in self.get_nome().lower() or "generico" in self.get_nome().lower()

    def get_necessita_prescricao(self):
        return "Sem Retenção De Receita" in self.page.content()
    
    def get_farmacia(self):
        return "farmafine"
