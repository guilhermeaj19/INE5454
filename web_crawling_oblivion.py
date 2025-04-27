
import unicodedata
import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
import re
import time

start = time.time()

base_url =  "https://en.uesp.net"
resposta = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def process_page(url: str):


  page_request = requests.get(url, headers=headers)
  page_content = page_request.content
  site = BeautifulSoup(page_content, 'html.parser')
  quests = site.find("div", {"id": "mw-pages"})
  quests = quests.find_all("div", {"class": "mw-category-group"})
  for group in quests:

    quests_in_group = group.find_all("a")

    for quest in quests_in_group:
      name = re.sub(r"Oblivion:(\w+)", r"\1", quest["title"])
      url = base_url + quest["href"]
      resposta.append({"Name": name, "URL": url})

  # print(f"Encontrado jogo {i}\n\tNome\t\t: {result['Name']} \n\tURL\t\t: {result['url']} \n\tPublicação\t: {result['Date']} \n\tMetascore\t: {result['Metacritic']}")

process_page("https://en.uesp.net/w/index.php?title=Category:Oblivion-Quests&pageuntil=To+Serve+Sithis#mw-pages")
process_page("https://en.uesp.net/w/index.php?title=Category:Oblivion-Quests&pagefrom=To+Serve+Sithis#mw-pages")
# dados_ordenados = sorted(dados, key=lambda x: x["Code"])
  # Converte os objetos Pyhton em objeto JSON e exporta para o jogos.json
with open('quests_oblivion.json', 'w', encoding="utf-8") as arquivo:
  arquivo.write(str(json.dumps(resposta, indent=4)))
print("Created Json File")
end = time.time()
print(f"Tempo de execução: {end - start:.2f} s")

import csv
with open("quests_oblivion.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["Name", "URL"]  # Definindo os nomes das colunas
    writer = csv.DictWriter(file, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)

    writer.writeheader()  # Escrevendo o cabeçalho
    writer.writerows(resposta)  # Escrevendo os dados

