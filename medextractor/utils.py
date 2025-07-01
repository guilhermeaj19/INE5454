import re, unicodedata

def strip_accents(txt: str) -> str:
    nfkd = unicodedata.normalize('NFKD', txt)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()

pattern = re.compile(r'(\d+)\s*(?:capsulas?|ml|saches?|comprimidos?)', re.IGNORECASE)

def extrai_qtd(texto):
    texto_norm = strip_accents(texto)
    m = pattern.search(texto_norm)
    return int(m.group(1)) if m else None
