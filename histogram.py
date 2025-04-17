import json
import matplotlib.pyplot as plt
from math import log10
import numpy as np

# Função para criar um histograma
def criar_histograma(nome_arquivo, chave):
    # Carregando o arquivo JSON
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    # Extraindo os valores associados à chave especificada
    valores = [item[chave] for item in dados if chave in item]
    print(sum(valores)/len(valores))
    n_bins = int(1 + 3.322 * log10(len(valores)))
    # Criando o histograma
    hist, edges = np.histogram(valores, bins=n_bins) 
    plt.hist(valores, bins=n_bins, edgecolor='black', color='skyblue')
    plt.xticks(edges)
    plt.title(f"Histograma da Nota dos jogos pelo {chave}")
    plt.xlabel("Metascore")
    plt.ylabel("Número de jogos")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Exibindo o histograma
    plt.show()

# Exemplo de uso
nome_arquivo = 'games.json'  # Substitua pelo nome do seu arquivo JSON
chave = 'Metacritic'         # Substitua pela chave cujos valores você deseja analisar
criar_histograma(nome_arquivo, chave)
