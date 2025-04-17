import unicodedata
import requests
import json
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool, set_start_method

months = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}
base_url = "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&page="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def process_page(page):
    print(f"Pagina {page} sendo analisada")
    resposta = []

    try:
        page_request = requests.get(base_url + str(page), headers=headers)
        page_content = page_request.content
        site = BeautifulSoup(page_content, 'html.parser')
        games = site.find_all("div", {"class": "c-finderProductCard c-finderProductCard-game"})

        for i, game in enumerate(games):
            result = {"Code": None, "Name": None, "Date": None, "url": None, "Metacritic": None}

            name = game.find("h3", {"class": "c-finderProductCard_titleHeading"})
            if name:
                code, name = name.find_all('span')
                code = re.sub(r"(\d+).", r"\1", code.get_text())
                result["Code"] = int(code)
                result["Name"] = name.get_text()
            else:
                continue

            score = game.find('span', {'data-v-e408cafe': True})
            result["Metacritic"] = int(score.get_text())

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
    except Exception as e:
        print(f"Erro na página {page}: {e}")
    return resposta

# Configuração principal do programa
if __name__ == '__main__':
    start = time.time()
    total_pages = 568
    with Pool(processes=8) as pool:  # Configuração de 8 processos paralelos
        all_results = pool.map(process_page, range(1, total_pages + 1))

    # Unir todas as respostas
    resposta_final = [item for sublist in all_results for item in sublist]

    # Exportar para JSON
    with open('games_multiprocess_1.json', 'w', encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(resposta_final, indent=4))

    print("Arquivo json criado")

    end = time.time()
    print(f"Tempo de execução: {end - start:.2f} s")
