import os
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

def buscar_anos_disponiveis():
   
    print(f"Investigando pasta raiz: {BASE_URL}")
    resposta = requests.get(BASE_URL)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    anos = []
    for link in soup.find_all('a'):
        texto = link.get('href')
        if texto and texto[0].isdigit() and texto.endswith('/'):
            ano_limpo = texto.strip('/')
            anos.append(ano_limpo)
    
    anos.sort(reverse=True)
    return anos

def baixar_arquivos():
    anos = buscar_anos_disponiveis()
    
    arquivos_para_baixar = []
    
    for ano in anos:
        if len(arquivos_para_baixar) >= 3:
            break 
            
        url_ano = f"{BASE_URL}{ano}/"
        print(f"Procurando arquivos em: {url_ano}")
        
        try:
            resp = requests.get(url_ano)
            soup_ano = BeautifulSoup(resp.text, 'html.parser')
            
            arquivos_do_ano = []
            for link in soup_ano.find_all('a'):
                nome_arquivo = link.get('href')
                
                
                if nome_arquivo.endswith('.zip'):
                    full_url = url_ano + nome_arquivo
                    arquivos_do_ano.append(full_url)
            

            arquivos_do_ano.sort(reverse=True)
            
            arquivos_para_baixar.extend(arquivos_do_ano)
            
        except Exception as e:
            print(f"Erro ao acessar ano {ano}: {e}")

    print(f"\n--- Encontrei {len(arquivos_para_baixar)} arquivos. Baixando os 3 mais recentes ---")
    
    os.makedirs("downloads", exist_ok=True)
    
    for url_arquivo in arquivos_para_baixar[:3]:
        nome_arquivo = url_arquivo.split('/')[-1]
        caminho_salvar = os.path.join("downloads", nome_arquivo)
        
        print(f"Baixando: {nome_arquivo}...")
        
        r = requests.get(url_arquivo, stream=True)
        with open(caminho_salvar, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
    print("\nSUCESSO! Verifique a pasta 'downloads'.")

if __name__ == "__main__":
    baixar_arquivos()