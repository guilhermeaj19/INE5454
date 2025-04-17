import unicodedata
import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
import re

base_url = "https://www.kabum.com.br/produto/"
resposta = []

for i in range(680000,680100):

  headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://www.kabum.com.br',
    'priority': 'u=1, i',
    'referer': 'https://www.kabum.com.br/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    # 'cookie': '__Secure-3PSID=g.a000uggLOnk15LB0z7GpeJ3vGNH2duB2SZjUOUbzzZm6p9ocaP2LhAbHjVq321k1_sDZBZqnlwACgYKAf0SARISFQHGX2Mi095SCFTv-A3EXVDT_SVDoxoVAUF8yKp0cXnkr5jGDwtcV69PKCA90076; __Secure-3PAPISID=DwRwkJQwxbPGmKp0/AOxBv3j1ZRkDQD6mI; __Secure-3PSIDTS=sidts-CjIB7pHptSo6OZOa4xGJl5y_un5OX32sRKKyW1WbrpPAdHk_tpFJl8zY9L-JKs23oTp56RAA; NID=522=kyYF0M6QcnX-hTykK1uKolEQaHtrE05ZbC9QSGQKVPjqBvmo2imJkQJi7SkkqL6CxRlocenU0oAflSG3SJSzqIa2ITPrDBn1CU3a_G5NZF9kKr_0Wcd46uKcdWfRoGeN-zyUunyYRi84bn5VWlbpMKFNA7amo96GHm4aWvsuBtt6aSCwJw5ZDrA4rGEUmDLyAKS2zxOR01ql_yQuucOFkb6LNGus3BxIYTJ1gMvrcnGyK6EutDeVh1bZTRYivPrBGtsGofTXak8h4d-EvlQDvVSd; __Secure-3PSIDCC=AKEyXzVj4TVnaLeqTeEDrMxQyWXNrUxA7Mjtu7hop9-9HgHZp8iJYLsr6a5qGRZNhPRXLvOziqA0',
}

  requisicaoDePagina = requests.get('https://www.kabum.com.br/produto/' + str(i), headers=headers)

  conteudo = requisicaoDePagina.content

  #joga para a variável site todo o conteúdo da página passada pelo requests.get()
  site = BeautifulSoup(conteudo, 'html.parser')

  #joga para a variável noticias todos os elementos "article", que é onde está cada uma das manchetes do site princial
  noticias = site.find_all("article")

  # #faz um laço na lista noticias (no plural), atribuindo cada item da lista para a variável noticia (no singular)
  for noticia in noticias:
    result = {"Code": i, "Name": None, "Price": None}

    price = noticia.find("h4", {"class" : "sc-5492faee-2 ipHrwP finalPrice"})

    if price:
        price = price.get_text()
        price = re.sub(r"\.","",price)
        price = re.sub(r"\u00a0","",price)
    else:
        price = "Produto indisponível"

    result["Price"] = price
   
    name = noticia.find("span", {"class": "max-w-[230px] hidden text-xl font-bold text-black-800 truncate desktop:block"})

    if name:
        name = name.get_text()
        result["Name"] = name
        print(f"Encontrado produto {i}, {result['Name']}: {result['Price']}")
        resposta.append(result) 

  # Converte os objetos Pyhton em objeto JSON e exporta para o noticias.json
with open('eletronics.json', 'w', encoding="utf-8") as arquivo:
  arquivo.write(str(json.dumps(resposta, indent=4)))
print("Created Json File")

