from urlextractor.abs_url_extractor import AbsUrlExtractor


class PrecoPopularUrlExtractor(AbsUrlExtractor):

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://www.precopopular.com.br/"

    def process(self, data):
        self.page.goto(data)
        self.page.wait_for_load_state("networkidle")

        for i in range(10):
            self.page.evaluate(f"window.scrollTo(0, document.body.scrollHeight/{10-i})")
            self.page.wait_for_timeout(200)
        box_url = "a.vtex-product-summary-2-x-clearLink.vtex-product-summary-2-x-clearLink--product__summary.vtex-product-summary-2-x-clearLink--product__summary--shelf.h-100.flex.flex-column"

        # Waiting all elements (starts loading 8 then 32) loads 5 times
        # If it not loads, assumes final page
        tries = 1
        while self.page.locator(box_url).count() < 9:
            print(f"waiting for the {tries} time; {self.page.locator(box_url).count()} urls")
            if tries >= 5:
                break
            self.page.wait_for_timeout(5000)
            tries += 1

    def get_urls(self):
        urls = self.page.locator("a.vtex-product-summary-2-x-clearLink.vtex-product-summary-2-x-clearLink--product__summary.vtex-product-summary-2-x-clearLink--product__summary--shelf.h-100.flex.flex-column").all()
        
        return [self.base_url + url.get_attribute('href') for url in urls]
