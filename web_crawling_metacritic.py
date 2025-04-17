
import unicodedata
import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
import re
import time

start = time.time()

base_url = "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&page="
resposta = []
total_pages = 568
months = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for page in range(1,total_pages+1):
  print(f"Pagina {page} sendo analisada")
  page_request = requests.get(base_url + str(page), headers=headers)
  page_content = page_request.content
  site = BeautifulSoup(page_content, 'html.parser')
  games = site.find_all("div", {"class": "c-finderProductCard c-finderProductCard-game"})

  for i, game in enumerate(games):
      result = {"Code": None, "Name": None, "Date": None, "url": None, "Metacritic": None}

      # Extração de nome
      name = game.find("h3", {"class": "c-finderProductCard_titleHeading"})
      if name:
          code, name = name.find_all('span')
          code = re.sub(r"(\d+).", r"\1", code.get_text())
          result["Code"] = int(code)
          result["Name"] = name.get_text()
      else:
          continue

      # Extração de Metacritic
      score = game.find('span', {'data-v-e408cafe': True})
      result["Metacritic"] = int(score.get_text())

      # Extração de data
      date = game.find('div', {"class": "c-finderProductCard_meta"})
      date = date.find('span', {"class": "u-text-uppercase"})
      date = date.get_text().strip()
      result_date = re.match(r"([A-Za-z]{3}) (\d{1,2}), (\d{4})", date)
      if result_date:
          month, day, year = result_date.groups()
          result["Date"] = f"{day}/{months[month]}/{year}"

      url = game.find("a", {"class": "c-finderProductCard_container"})
      result["url"] = "metacritic.com" + url['href']

      resposta.append(result)
    # print(f"Encontrado jogo {i}\n\tNome\t\t: {result['Name']} \n\tURL\t\t: {result['url']} \n\tPublicação\t: {result['Date']} \n\tMetascore\t: {result['Metacritic']}")

# dados_ordenados = sorted(dados, key=lambda x: x["Code"])
  # Converte os objetos Pyhton em objeto JSON e exporta para o jogos.json
with open('games.json', 'w', encoding="utf-8") as arquivo:
  arquivo.write(str(json.dumps(resposta, indent=4)))
print("Created Json File")
end = time.time()
print(f"Tempo de execução: {end - start:.2f} s")

