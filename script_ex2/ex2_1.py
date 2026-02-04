import pandas as pd
import zipfile
import io
import re
import os

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', str(cnpj))
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False
    def calcular_digito(fatia, pesos):
        soma = sum(int(a) * b for a, b in zip(fatia, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    if int(cnpj[12]) != calcular_digito(cnpj[:12], pesos1):
        return False
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    if int(cnpj[13]) != calcular_digito(cnpj[:13], pesos2):
        return False
    return True

def executar():
    print(" Iniciando Exercício 2.1: Validação de Dados...")

    caminho_zip = 'output/consolidado_despesas.zip'
    
    if not os.path.exists(caminho_zip):
        print(f"Erro: O arquivo '{caminho_zip}' não foi encontrado!")
        print("Certifique-se de que o arquivo está dentro da pasta 'output'.")
        return

    try:
        with zipfile.ZipFile(caminho_zip, 'r') as z:
            nome_csv = z.namelist()[0] # Pega o primeiro arquivo dentro do zip
            with z.open(nome_csv) as f:
                df = pd.read_csv(f, sep=None, engine='python')
        
        print(f" Arquivo '{nome_csv}' extraído do ZIP com {len(df)} linhas.")
    except Exception as e:
        print(f" Erro ao ler o ZIP: {e}")
        return

    df.columns = [c.strip() for c in df.columns]

    print("🔍 Aplicando regras de validação...")
    
    mask_razao_ok = df['RazaoSocial'].notna() & (df['RazaoSocial'].astype(str).str.strip() != "")
    
    df['ValorDespesas'] = pd.to_numeric(df['ValorDespesas'], errors='coerce').fillna(0)
    mask_valor_ok = df['ValorDespesas'] > 0
    
    mask_cnpj_valido = df['CNPJ'].apply(validar_cnpj)

    mask_total = mask_razao_ok & mask_valor_ok & mask_cnpj_valido
    df_final = df[mask_total].copy()
    df_quarentena = df[~mask_total].copy()

    df_final.to_csv('output/consolidado_despesas.csv"', index=False, encoding='utf-8-sig')
    df_quarentena.to_csv('output/quarentena_erros.csv', index=False, encoding='utf-8-sig')

    print(f"\n--- Relatório Final ---")
    print(f"Registros Válidos: {len(df_final)}")
    print(f"Registros em Quarentena: {len(df_quarentena)}")
    print(f"Arquivos salvos em 'output/'")

if __name__ == "__main__":
    executar()