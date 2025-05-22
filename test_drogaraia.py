from extractors.drogaraia import DrogaraiaExtractor
from medextractor.helpers import AbsMedExtractor
from playwright.sync_api import sync_playwright


def print_meds(urls: list[str], extractor: AbsMedExtractor):
    for data in urls:
        med = extractor.get(data)
        print(med, end = "\n\n")

# Base: https://www.drogaraia.com.br/medicamentos/remedios.html
med_urls_drogaraia = ["https://www.drogaraia.com.br/tadalafila-20mg-neo-quimica-generico-1-comprimidos-revestidos.html",
                      "https://www.drogaraia.com.br/montelair-4mg-60-saches.html",
                      "https://www.drogaraia.com.br/dipirona-sodica-ems-gen-500mg-1x10-comprimidos.html",
                      "https://www.drogaraia.com.br/espran-10-mg-30-comprimidos-c1.html",
                      "https://www.drogaraia.com.br/drusolol-solucao-oftalmica-5-ml.html",
                      "https://www.drogaraia.com.br/spray-gengibre-e-hortela-35ml-natusday-1066023.html"]

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()

print("Medicamentos Drogaraia")
drogaraia_extractor = DrogaraiaExtractor(page)
print_meds(med_urls_drogaraia, drogaraia_extractor)
print(f"{''.join(['=']*150)}")

pw.stop()
