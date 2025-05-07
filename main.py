from dataclasses import asdict
from extractors.preco_popular import PrecoPopularExtractor

extractor = PrecoPopularExtractor()

med_urls = ["https://www.precopopular.com.br/vitamina-d3-neo-quimica-com-8-capsulas-50000ui/p",
            "https://www.precopopular.com.br/nevralgex-com-30-comprimidos/p",
            "https://www.precopopular.com.br/aberalgina-dipirona-monoidratada-20ml-solucao-oral-500mg-ml/p",
            "https://www.precopopular.com.br/antiacido-em-pastilha-gastrol-10-comprimidos-mastigaveis/p",
            "https://www.precopopular.com.br/prednisona-medley-com-10-comprimidos-20mg-genericos/p",
            "https://www.precopopular.com.br/miconazol-creme-28g/p",
            "https://www.precopopular.com.br/elani-28-com-84-comprimidos/p",
            "https://www.precopopular.com.br/slinda-com-72-12-comprimidos-revestidos-4mg/p",
            "https://www.precopopular.com.br/dexametasona-ems-4mg-com-10-comprimidos/p",
            "https://www.precopopular.com.br/espironolactona-eurofarma-50mg-com-30-comprimidos/p"]

for data in med_urls:
    med = extractor.get(data)
    print(med, end = "\n\n")

