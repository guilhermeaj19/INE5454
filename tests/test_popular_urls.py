import sys
sys.path.append("C:/Users/guilh/OneDrive/Documentos/GitHub/INE5454")


from urlextractor.preco_popular_url_extractor import PrecoPopularUrlExtractor
from playwright.sync_api import sync_playwright, TimeoutError

def get_page(extractor, i):
    try:
        return extractor.get(f"https://www.precopopular.com.br/medicamentos?page={i}")

    except TimeoutError as e:
        print(f"Error: {e}")
        return get_page(extractor, i)

def get(extractor):
    resposta = []
    i = 1
    while True:
        result = get_page(extractor, i)
        if len(result) == 0:
            break
        print(i, len(result))
        resposta += result
        i += 1
    return resposta    


pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=True)
page = chrome.new_page()

extractor = PrecoPopularUrlExtractor(page)
get(extractor)
