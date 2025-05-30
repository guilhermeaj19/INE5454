import sys
sys.path.append("C:/Users/guilh/OneDrive/Documentos/GitHub/INE5454")


from extractors.drogaraia import DrogaraiaExtractor
from playwright.sync_api import sync_playwright, TimeoutError
import json
from multiprocessing import Pool

def get_meds(urls, extractor):
    print(f"Acessando urls da página {list(urls.keys())[0]}")
    meds = []
    for urls_ in urls.values():
        for url in urls_:
            med = get_med(url, extractor)
            print(med)
            meds.append(med)

    return meds

def get_med(url, extractor: DrogaraiaExtractor):
    try:
        return extractor.get(url)
    except TimeoutError as e:
        print(f"Error: {e}")
        return get_med(url, extractor)

with open("urlextractor/drogaria.json", 'r', encoding= "utf-8") as file:
    urls = json.load(file)

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
# extractors = [DrogaraiaExtractor(chrome.new_page()) for _ in range(8)]
extractor = DrogaraiaExtractor(chrome.new_page())
# with Pool(processes=8) as pool:
#     meds = pool.map(get_meds, (urls, extractors))
meds = []
for i in range(5):
    meds += get_meds(urls[i], extractor)

print(meds)
# print("Medicamentos Drogaraia")
# drogaraia_extractor = DrogaraiaExtractor(page)
# print_meds(med_urls_drogaraia, drogaraia_extractor)
# print(f"{''.join(['=']*150)}")

pw.stop()
