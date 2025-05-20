from extractors.preco_popular import PrecoPopularExtractor
from extractors.panvel import PanvelExtractor
from extractors.catarinense import CatarinenseExtractor
from medextractor.helpers import AbsMedExtractor
from playwright.sync_api import sync_playwright

def print_meds(urls: list[str], extractor: AbsMedExtractor):
    for data in urls:
        med = extractor.get(data)
        print(med, end = "\n\n")

# Base: https://www.precopopular.com.br/medicamentos
med_urls_popular = ["https://www.precopopular.com.br/vitamina-d3-neo-quimica-com-8-capsulas-50000ui/p",
                    "https://www.precopopular.com.br/nevralgex-com-30-comprimidos/p",
                    "https://www.precopopular.com.br/aberalgina-dipirona-monoidratada-20ml-solucao-oral-500mg-ml/p",
                    "https://www.precopopular.com.br/antiacido-em-pastilha-gastrol-10-comprimidos-mastigaveis/p",
                    "https://www.precopopular.com.br/prednisona-medley-com-10-comprimidos-20mg-genericos/p",
                    "https://www.precopopular.com.br/miconazol-creme-28g/p",
                    "https://www.precopopular.com.br/elani-28-com-84-comprimidos/p",
                    "https://www.precopopular.com.br/slinda-com-72-12-comprimidos-revestidos-4mg/p",
                    "https://www.precopopular.com.br/dexametasona-ems-4mg-com-10-comprimidos/p",
                    "https://www.precopopular.com.br/espironolactona-eurofarma-50mg-com-30-comprimidos/p"]

# Base: https://www.drogariacatarinense.com.br/medicamentos
med_urls_catarinense = ["https://www.drogariacatarinense.com.br/tadalafila-ems-5mg-com-30-comprimidos/p",
                        "https://www.drogariacatarinense.com.br/dipirona-ems-500mg-com-10-comprimidos/p",
                        "https://www.drogariacatarinense.com.br/albendazol-medley-com-3-comprimidos-mastigaveis-400mg-generico/p",
                        "https://www.drogariacatarinense.com.br/omeprazol-20mg-teuto-com-56-capsulas/p",
                        "https://www.drogariacatarinense.com.br/aspirina-prevent-100mg-com-30-comprimidos/p",
                        "https://www.drogariacatarinense.com.br/avamys-spray-nasal-120-doses/p",
                        "https://www.drogariacatarinense.com.br/complexo-almeida-prado-46-com-60-comprimidos/p",
                        "https://www.drogariacatarinense.com.br/xarope-de-guaco-g500-balsamico-150ml/p",
                        "https://www.drogariacatarinense.com.br/suplemento-neo-quimica-vitamina-c-500mg-30-comprimidos/p",
                        "https://www.drogariacatarinense.com.br/dipirona-medley-solucao-100ml/p"]

# Base: https://www.panvel.com/panvel/medicamentos/c-35206
med_urls_panvel = ["https://www.panvel.com/panvel/durateston-250mg-ml-1ml-1-ampola-c5/p-655",
                   "https://www.panvel.com/panvel/maleato-enalapril-10mg-30-comprimidos-nova-quimica-generico/p-106657",
                   "https://www.panvel.com/panvel/aripiprazol-10mg-30-comprimidos-prati-donaduzzi-generico-c1/p-107992",
                   "https://www.panvel.com/panvel/dipirona-sodica-monoidratada-500mg-ml-10ml-medquimica-generico/p-106847",
                   "https://www.panvel.com/panvel/praalergia-180mg-6-comprimidos-revestidos-cimed/p-93669",
                   "https://www.panvel.com/panvel/oleo-mineral-100-lifar/p-94219",
                   "https://www.panvel.com/panvel/furosemida-40mg-20-comprimidos-prati-donaduzzi-generico/p-107765",
                   "https://www.panvel.com/panvel/agulha-para-caneta-de-insulina-novo-fine-32g-4mm-com-7-unidades/p-92499",
                   "https://www.panvel.com/panvel/reidratante-sorox-tangerina-550ml/p-93175"]

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=True)
page = chrome.new_page()

print("Medicamentos Preço Popular")
popular_extractor = PrecoPopularExtractor(page)
print_meds(med_urls_popular, popular_extractor)
print(f"{''.join(['=']*150)}")

print("Medicamentos Drogaria Catarinense")
catarinense_extractor = CatarinenseExtractor(page)
# Parece que o extrator da Preço Popular também funciona para Drogaria Catarinense
# Realizar mais testes para confirmar se vale para todos os atributos
print_meds(med_urls_catarinense, catarinense_extractor)
print(f"{''.join(['=']*150)}")

print("Medicamentos Panvel")
panvel_extractor = PanvelExtractor(page)
print_meds(med_urls_panvel, panvel_extractor)

pw.stop()
