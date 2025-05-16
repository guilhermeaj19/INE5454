import requests
from medextractor.helpers import AbsMedExtractor

class CatarinenseExtractor(AbsMedExtractor):
    def __init__(self, page):
        super().__init__(page)

    def process(self, data):
        self.page.goto(data)
        self.page.wait_for_selector("span.vtex-product-price-1-x-currencyFraction--product__price")

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
            return self.page.locator(
                        "a.precopopular-apps-common-components-2-x-productSpecificationContentValueLink"
                    ).first.text_content(timeout=5000)
        except:
            return None
    
    def get_image_source(self):
        return self.page.locator(
            "img.vtex-store-components-3-x-productImageTag"
        ).first.get_attribute("src")


