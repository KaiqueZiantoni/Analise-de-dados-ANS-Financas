import pandas as pd
import zipfile
import os


ARQUIVO_CONTABIL = 'dados_consolidados.csv'
ARQUIVO_CADASTRO = 'Relatorio_Cadop.csv' 
ARQUIVO_SAIDA_ZIP = 'output/consolidado_despesas.zip'
NOME_CSV_INTERNO = 'consolidado_despesas.csv'


def executar():
    print(">>> Iniciando Carregamento dos Dados...")

    try:
        df_contabil = pd.read_csv(ARQUIVO_CONTABIL, sep=None, engine='python')
        print(f"Sucesso: {ARQUIVO_CONTABIL} carregado com {len(df_contabil)} linhas.")
        df_contabil.columns = df_contabil.columns.str.strip()
    
    except FileNotFoundError:
        print(f"ERRO: Não encontrei '{ARQUIVO_CONTABIL}'.")
        return

    print(f">>> Lendo {ARQUIVO_CADASTRO}...")
    try:
        df_cadop = pd.read_csv(ARQUIVO_CADASTRO, sep=';', encoding='utf-8-sig', header=None, usecols=[0, 1, 2])    
        df_cadop.columns = ['REGISTRO_ANS_JOIN', 'CNPJ', 'RAZAO_SOCIAL']
        print(f"Cadastro carregado: {len(df_cadop)} operadoras.")

    except Exception as e:
        print(f"ERRO ao ler cadastro: {e}")
        try:
            df_cadop = pd.read_csv(ARQUIVO_CADASTRO, sep=';', encoding='utf-8-sig', header=None, usecols=[0, 1, 2])
            df_cadop.columns = ['REGISTRO_ANS_JOIN', 'CNPJ', 'RAZAO_SOCIAL']
        except Exception as e2:
            print(f"ERRO FATAL NO CADASTRO: {e2}")
            exit()

    print(">>>  Realizando o cruzamento (Merge)...")

    df_contabil['REGISTRO_ANS'] = pd.to_numeric(df_contabil['REGISTRO_ANS'], errors='coerce')
    df_cadop['REGISTRO_ANS_JOIN'] = pd.to_numeric(df_cadop['REGISTRO_ANS_JOIN'], errors='coerce')


    df_merged = pd.merge(
        df_contabil,
        df_cadop,
        left_on='REGISTRO_ANS',
        right_on='REGISTRO_ANS_JOIN',
        how='inner'
    )

    print(">>>  Aplicando regras de negócio...")

    df_merged['DATA_REFERENCIA'] = pd.to_datetime(df_merged['DATA_REFERENCIA'], errors='coerce')
    df_merged['Ano'] = df_merged['DATA_REFERENCIA'].dt.year
    df_merged['Trimestre'] = df_merged['DATA_REFERENCIA'].dt.quarter

    if df_merged['VALOR'].dtype == 'object':
        df_merged['VALOR'] = df_merged['VALOR'].astype(str).str.replace(',', '.', regex=False)

    df_merged['VALOR'] = pd.to_numeric(df_merged['VALOR'], errors='coerce')

    df_final = df_merged[df_merged['VALOR'] != 0].copy()
    df_final = df_final.dropna(subset=['VALOR', 'CNPJ'])

    df_final = df_final.rename(columns={'VALOR': 'ValorDespesas', 'RAZAO_SOCIAL': 'RazaoSocial'})
    colunas_finais = ['CNPJ', 'RazaoSocial', 'Trimestre', 'Ano', 'ValorDespesas']

    cols_existentes = [c for c in colunas_finais if c in df_final.columns]
    df_export = df_final[cols_existentes]

    print(f">>>  Gerando ZIP final com {len(df_export)} registros...")

    with zipfile.ZipFile(ARQUIVO_SAIDA_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        csv_data = df_export.to_csv(index=False, sep=';', encoding='utf-8-sig')
        zf.writestr(NOME_CSV_INTERNO, csv_data)

    print(f"\n Arquivo '{ARQUIVO_SAIDA_ZIP}' gerado na pasta.")


    if __name__ == "__main__":
        executar()