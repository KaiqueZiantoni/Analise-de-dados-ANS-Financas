import pandas as pd

print(">>> DIAGNÓSTICO DO ARQUIVO DADOS_CONSOLIDADOS.CSV <<<")

try:

    df = pd.read_csv('dados_consolidados.csv', sep=None, engine='python', nrows=5)
    
    print("\n1. AS COLUNAS QUE O PANDAS ENCONTROU:")
    print(df.columns.tolist())
    
    print("\n2. COMO ESTÃO OS DADOS (Primeira linha):")
    print(df.head(1))

except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")