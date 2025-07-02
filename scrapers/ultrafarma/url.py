import time
from medextractor import AbsUrlExtractor
import json

class UltrafarmaUrlExtractor(AbsUrlExtractor):

    def __init__(self, url=None):
        super().__init__(url if url else "https://www.ultrafarma.com.br/categoria/medicamentos", limit=600)

    def setup(self):
        self.page.goto(self.url if self.url else "")
        self.page.wait_for_selector("a.product-item-link")
        self.previous_height = self.page.evaluate("document.body.scrollHeight")

    def get_next_url(self):
        #Infinite scroll
        group_buttons = self.page.locator("div.group-inputs-button")
        group_buttons.scroll_into_view_if_needed()
        for i in range(20):
            current_height = self.page.evaluate("document.body.scrollHeight")
            if current_height != self.previous_height:
                self.previous_height = current_height
                return ""
            time.sleep(0.5)

        return None

    def get_urls(self):
        # urls_element = self.page.locator("a.product-item-link").all()
        urls_element = self.page.evaluate(
    """
    ({selector, count}) => {
        const nodes = Array.from(document.querySelectorAll(selector));
        return nodes.slice(-count).map(el => ({
            href: el.href,
            text: el.textContent.trim()
        }));
    }
    """,
    {"selector": "a.product-item-link", "count": 50}
)
        urls = [url["href"] for url in urls_element]
        return urls
        # with open("urlextractor/drogaria.jsonl", 'w', encoding="utf-8") as file:
        #     file.write(str(json.dumps({1: [url.get_attribute('href') for url in urls_element]}, indent=4)))
            
        #     for i in range(2, 192):
        #         self.process(self.url + str(i))
        #         urls_element = self.page.locator("div.ProductCardstyles__ContainerImage-iu9am6-1.wXbdy a").all()
        #         file.write(str(json.dumps({i: [url.get_attribute('href') for url in urls_element]}, indent=4))+'\n')