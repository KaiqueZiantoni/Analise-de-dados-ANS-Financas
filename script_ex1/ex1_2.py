import os
import zipfile
import pandas as pd

PASTA_DOWNLOADS = './downloads'
ARQUIVO_SAIDA = 'dados_consolidados.csv'

MAPA_COLUNAS = {
    'DATA': 'DATA_REFERENCIA',
    'dt_ref': 'DATA_REFERENCIA',
    'REG_ANS': 'REGISTRO_ANS',
    'CD_CONTA': 'CODIGO_CONTA',
    'CD_CONTA_CONTABIL': 'CODIGO_CONTA', 
    'DS_CONTA': 'DESCRICAO_CONTA',
    'DESCRICAO': 'DESCRICAO_CONTA',    
    'VL_SALDO_FINAL': 'VALOR',
    'vl_saldo_final': 'VALOR'
}

def normalizar_colunas(df):
    df.columns = [c.strip() for c in df.columns]
    df.rename(columns=MAPA_COLUNAS, inplace=True)
    return df

def carregar_arquivo_generico(arquivo_bytes, nome_arquivo):
    nome_arquivo = nome_arquivo.lower()
    try:
        if nome_arquivo.endswith('.csv') or nome_arquivo.endswith('.txt'):
            try:
                return pd.read_csv(arquivo_bytes, sep=';', encoding='utf-8-sig', thousands='.', decimal=',')
            except:
                arquivo_bytes.seek(0)
                return pd.read_csv(arquivo_bytes, sep=',', encoding='utf-8-sig')
        elif nome_arquivo.endswith('.xlsx'):
            return pd.read_excel(arquivo_bytes)
    except Exception as e:
        print(f"Erro ao ler {nome_arquivo}: {e}")
        return None

def executar():
    arquivos_zip = [f for f in os.listdir(PASTA_DOWNLOADS) if f.endswith('.zip')]
    arquivos_zip.sort(reverse=True)
    
    dfs_processados = []

    for zip_nome in arquivos_zip:
        caminho_zip = os.path.join(PASTA_DOWNLOADS, zip_nome)
        print(f"\n>>> Processando ZIP: {zip_nome}")
        
        with zipfile.ZipFile(caminho_zip, 'r') as z:
            for nome_arquivo in z.namelist():
                if 'pdf' in nome_arquivo.lower() or 'leia' in nome_arquivo.lower():
                    continue
                
                print(f"   Lendo: {nome_arquivo}...")
                with z.open(nome_arquivo) as f:
                    df = carregar_arquivo_generico(f, nome_arquivo)
                    
                    if df is not None:
                        df = normalizar_colunas(df)
                        
                        if 'DESCRICAO_CONTA' in df.columns:
                            filtro = df['DESCRICAO_CONTA'].astype(str).str.contains('EVENTOS|SINISTROS', case=False, na=False)
                            df_filtrado = df[filtro].copy()
                            df_filtrado['ARQUIVO_ORIGEM'] = nome_arquivo
                            
                            print(f"   -> Linhas originais: {len(df)} | Linhas filtradas (Sinistros): {len(df_filtrado)}")
                            
                            if not df_filtrado.empty:
                                dfs_processados.append(df_filtrado)
                        else:
                            print("   [!] Coluna 'DESCRICAO_CONTA' não encontrada após normalização.")

    if dfs_processados:
        print("\n--- Consolidando dados ---")
        df_final = pd.concat(dfs_processados, ignore_index=True)
        
        print(f"Total de registros consolidados: {len(df_final)}")
        print(f"Salvando em {ARQUIVO_SAIDA}...")
        
        df_final.to_csv(ARQUIVO_SAIDA, index=False, sep=';', encoding='utf-8')
        print("Sucesso! ETL Concluído.")
    else:
        print("Nenhum dado relevante encontrado.")

if __name__ == "__main__":
    executar()