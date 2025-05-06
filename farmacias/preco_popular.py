import requests
import json
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool, set_start_method
from playwright.sync_api import sync_playwright

months = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}
base_url = "https://www.precopopular.com.br"
base_url_meds_page = "/medicamentos?page="

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def process_product(product_ref_url):
    print(f"Produto {product_ref_url}")
    resposta = dict()
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(base_url + product_ref_url, timeout=60000, wait_until='domcontentloaded')

            # Wait for a specific element to be present (more reliable)
            # page.wait_for_selector(".vtex-flex-layout-0-x-flexRow--product__main", state="visible", timeout=60000)
            # print("Main Box found")

            time.sleep(3)
            page.wait_for_selector("vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product__price", state="visible", timeout=10000)
            print("Price Box found")
            
            # Get the updated page source after JavaScript execution
            page_content = page.content()
            site = BeautifulSoup(page_content, 'html.parser')

            med_main = site.find("div", {"class": "vtex-flex-layout-0-x-flexRow--product__main"})
            med_name = med_main.find("span", {"class": "vtex-store-components-3-x-productBrand"})
            med_code = med_main.find("span", {"class": "vtex-product-identifier-0-x-product-identifier__value"})
            
            med_price_box = med_main.find("span", {"class": "vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product__price"})
            # while not med_price_box:
            #     print(f"Product {product_ref_url} price doesn't found")
            #     time.sleep(2)
            #     page_content = page.content()
            #     site = BeautifulSoup(page_content, 'html.parser')
            #     med_main = site.find("div", {"class": "vtex-flex-layout-0-x-flexRow--product__main"})
            #     med_main.find("span", {"class": "vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product__price"})
            
            med_price_integer = med_price_box.find("span", {"class": "vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--product__price"})
            med_price_fraction = med_price_box.find("span", {"class": "vtex-product-price-1-x-currencyFraction vtex-product-price-1-x-currencyFraction--product__price"})

            print(f"Produto: {med_code.get_text()} : {med_name.get_text()} : {med_price_integer.get_text()},{med_price_fraction.get_text()}")
            resposta["nome"] = med_name.get_text()
            resposta["code"] = med_code.get_text()
            resposta["price"] = float(f"{med_price_integer.get_text()}.{med_price_fraction.get_text()}")

        except Exception as e:
            print(f"Error: {e}")

    return resposta

def process_page(page):
    # # print(f"Pagina {page} sendo analisada")
    # with sync_playwright() as p:
    #     browser = p.firefox.launch(headless=True)
    #     page = browser.new_page()

    #     try:
    #         page.goto(base_url + base_url_meds_page + str(page), timeout=60000, wait_until='domcontentloaded')

    #         # Wait for a specific element to be present (more reliable)
    #         page.wait_for_selector(".vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product__summary vtex-product-summary-2-x-clearLink--product__summary--shelf h-100 flex flex-column", state="visible", timeout=60000)
    #         print("Main Box found")

    #         # page.wait_for_selector(".galley-layout-containeir", state="visible", timeout=10000)
    #         # print("Price Box found")
            
    #         # Get the updated page source after JavaScript execution
    #         page_content = page.content()
    #         # page_request = requests.get(base_url + base_url_meds_page + str(page), headers=headers)
    #         # page_content = page_request.content
    #         site = BeautifulSoup(page_content, 'html.parser')
    #         meds_box = site.find("div", {"id": "gallery-layout-container"})
    #         meds = meds_box.find_all("a", {"class": "vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product__summary vtex-product-summary-2-x-clearLink--product__summary--shelf h-100 flex flex-column"})
    #         print(page, len([med["href"] for med in meds]))
    #         return [med["href"] for med in meds]
    
    #     except Exception as e:
    #         print(f"Erro na página {page}: {e}")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page_instance = browser.new_page()
        urls_on_page = []
        try:
            page_instance.goto(base_url + base_url_meds_page + str(page), timeout=6000, wait_until='domcontentloaded')
            page_instance.wait_for_selector("#gallery-layout-container", state="visible", timeout=6000)
            print("Main Container found")

            # Wait for up to a longer time for the elements to load
            try:
                page_instance.wait_for_selector("#gallery-layout-container a.vtex-product-summary-2-x-clearLink:nth-child(32)", state="visible", timeout=20000)
                print("Attempted to wait for 32 product links")
            except Exception:
                print("Did not find 32 product links within the extended timeout, proceeding.")

            page_content = page_instance.content()
            soup = BeautifulSoup(page_content, 'html.parser')
            meds_box = soup.find("div", {"id": "gallery-layout-container"})
            if meds_box:
                meds = meds_box.find_all("a", {"class": "vtex-product-summary-2-x-clearLink"})
                urls_on_page = [med["href"] for med in meds if "href" in med.attrs and med["href"].startswith("/")]
            print(f"Page {page}: Found {len(urls_on_page)} URLs")

        except Exception as e:
            print(f"Erro na página {page}: {e}")
        finally:
            browser.close()
        return urls_on_page

# Configuração principal do programa
if __name__ == '__main__':
    start = time.time()
    all_url_products = []
    process_page(1)
    exit()
    page = 1
    pages_analyzed = 0
    pool_processes = Pool(processes=8)
    while True:
        pages_to_process = range(page, page + 8)
        results_from_batch = pool_processes.map(process_page, pages_to_process)

        new_urls_found = False
        for urls in results_from_batch:
            if urls:
                all_url_products.extend(urls)
                pages_analyzed += 1
                new_urls_found = True

        if not new_urls_found and page > 1: # Break if no new URLs found in a batch after the first page
            break

        page += 8

    
    print(f"Number of pages: {pages_analyzed}")
    print(f"Number of products: {len(all_url_products)}")


    # all_results = pool_processes.map(process_product, all_url_products)

    # Unir todas as respostas
    # resposta_final = [item for sublist in all_results for item in sublist]

    # Exportar para JSON
    with open('meds_preco_popular.json', 'w', encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(all_url_products, indent=4))

    print("Arquivo json criado")

    end = time.time()
    print(f"Tempo de execução: {end - start:.2f} s")
