import requests
from medextractor.helpers import AbsMedExtractor

class CatarinenseExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)
        self.page.wait_for_selector("span.vtex-product-price-1-x-currencyFraction--product__price")

        class_button = ".vtex-button.bw1.ba.fw5.v-mid.relative.pa0.lh-solid.br2.min-h-regular.t-action.bg-action-secondary.b--action-secondary.c-on-action-secondary.hover-bg-action-secondary.hover-b--action-secondary.hover-c-on-action-secondary.pointer"

        if self.page.is_visible(class_button, timeout=5000):
            self.page.locator(class_button).last.click()

    def get_nome(self):
        return self.page.locator("span.vtex-store-components-3-x-productBrand").first.text_content().strip()

    def get_preco(self):
        price_integer = self.page.locator("span.vtex-product-price-1-x-currencyInteger--product__price").last.text_content()
        price_fraction = self.page.locator("span.vtex-product-price-1-x-currencyFraction--product__price").last.text_content()
        price = float(f"{price_integer}.{price_fraction}")
        return price

    def get_code(self):
        return int(self.page.locator(
            "span.vtex-product-identifier-0-x-product-identifier__value").first.text_content()
        )
    
    def get_marca(self):
        return self.page.locator(
                    "span.vtex-store-components-3-x-productBrandName"
                ).first.text_content()

    def get_categoria(self):
        return self.page.locator(
                    "a.vtex-breadcrumb-1-x-link--2"
                ).first.text_content()
    
    def get_sub_categoria(self):
        try:
            return self.page.locator(
                        "a.vtex-breadcrumb-1-x-link--3"
                    ).first.text_content(timeout=5000)
        except:
            return None
    
    def get_principios_ativos(self):
        try:
            principios_ativos = [locator.text_content(timeout=5000) for locator in self.page.locator(
                    "a.precopopular-apps-common-components-2-x-productSpecificationContentValueLink"
                ).all()]           
             
            if len(principios_ativos) > 0:
                return principios_ativos
            else:
                return None
        except Exception as e:
            return None
    
    def get_image_source(self):
        return self.page.locator(
            "img.vtex-store-components-3-x-productImageTag"
        ).first.get_attribute("src")

    def get_is_generico(self):
        try:
            # box_1 = "//div[contains(@style, 'border: 1px solid #000000; padding: 10px; border-radius: 10px; text-align: center;')] //span[contains(@style, 'font-size: small;')]"
            box_2 = "//div[contains(@style, 'border: 1px solid #000000; padding: 10px; border-radius: 10px;  text-align: center;')] //span[contains(@style, 'font-size: small;')]"
            # if self.page.is_visible(box_1, timeout=5000):
            #     if "MEDICAMENTO GENÉRICO" in self.page.locator(box_1).text_content():
            #         print("GENERICO: BOX 1")
            #         return True
        
            if self.page.is_visible(box_2, timeout=5000):
                if "MEDICAMENTO GENÉRICO" in self.page.locator(box_2).text_content():
                    print("GENERICO: BOX 2")
                    return True
            
            return False
        except Exception as e:
            return False

    def get_necessita_prescricao(self):
        try:
            box_1 = "//div[contains(@style, 'border: 1px solid #000000; padding: 10px; border-radius: 10px; text-align: center;')] //span[contains(@style, 'font-size: small;')]"
            box_2 = "//div[contains(@style, 'border: 1px solid #000000; padding: 10px; border-radius: 10px;  text-align: center;')] //span[contains(@style, 'font-size: small;')]"
            if self.page.is_visible(box_1, timeout=5000):
                if "PRESCRIÇÃO MÉDICA" in self.page.locator(box_1).text_content():
                    print("PRESCRICAO: BOX 1")
                    return True
        
            if self.page.is_visible(box_2, timeout=5000):
                if "PRESCRIÇÃO MÉDICA" in self.page.locator(box_2).text_content():
                    print("PRESCRICAO: BOX 2")
                    return True
            
            return False
        except Exception as e:
            return False