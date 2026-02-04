import pandas as pd
import os

def executar():
    print("-" * 40)
    print("Iniciando Etapa 2.2: Enriquecimento de Dados...")
    
    path_validados = 'output/consolidado_despesas.csv'
    path_cadop = 'Registros_Ativos/operadoras_ativas.csv' 
    path_output = 'output/dados_enriquecidos.csv'
    path_quarentena_cadop = 'output/quarentena_cadastral.csv'

    if not os.path.exists(path_cadop):
        print(f"ERRO: Arquivo não encontrado em: {path_cadop}")
        return

    df_despesas = pd.read_csv(path_validados, dtype={'CNPJ': str})
    df_cadop = pd.read_csv(path_cadop, sep=';', encoding='iso-8859-1', dtype={'CNPJ': str})

    df_cadop.columns = df_cadop.columns.str.strip().str.upper().str.replace(' ', '_')
    

    col_registro = 'REGISTRO_OPERADORA' 
    
    if col_registro not in df_cadop.columns:
        print(f"❌ Erro crítico: A coluna {col_registro} não foi encontrada.")
        return

    print(f"✅ Coluna de registro identificada: {col_registro}")


    colunas_interesse = ['CNPJ', col_registro, 'MODALIDADE', 'UF']
    
    df_cadop_clean = df_cadop.drop_duplicates(subset=['CNPJ'], keep='last')

    print("Realizando cruzamento de dados (Join)...")
    df_final = pd.merge(
        df_despesas, 
        df_cadop_clean[colunas_interesse], 
        on='CNPJ', 
        how='left'
    )

    df_final = df_final.rename(columns={col_registro: 'REGISTRO_ANS'})

    mask_sem_match = df_final['REGISTRO_ANS'].isna()
    df_enriquecidos = df_final[~mask_sem_match]
    df_quarentena = df_final[mask_sem_match]

    os.makedirs('output', exist_ok=True)
    df_enriquecidos.to_csv(path_output, index=False, encoding='utf-8-sig')
    df_quarentena.to_csv(path_quarentena_cadop, index=False, encoding='utf-8-sig')

    print("-" * 40)
    print(f"SUCESSO!")
    print(f"Registros Enriquecidos: {len(df_enriquecidos)}")
    print(f"Registros sem Cadastro (Quarentena): {len(df_quarentena)}")
    print(f"Arquivos gerados na pasta 'output/'")
    print("-" * 40)

if __name__ == "__main__":
    executar()

