import requests
from bs4 import BeautifulSoup

url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

print(f"Acessando: {url}")

try:
    resposta = requests.get(url)    
    soup = BeautifulSoup(resposta.text, 'html.parser')
    print("\n--- O que tem dentro da pasta: ---")    
    for link in soup.find_all('a'):
        texto = link.get('href')
        if texto and texto != "../":
            print(texto)
except Exception as erro:
    print(f"Deu erro: {erro}")