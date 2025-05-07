from dataclasses import asdict
from extractors.preco_popular import PrecoPopularExtractor

extractor = PrecoPopularExtractor()
med = extractor.get("https://www.precopopular.com.br/vitamina-d3-neo-quimica-com-8-capsulas-50000ui/p")
print(med)