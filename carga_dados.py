import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:SuaSenha123@localhost:5432/postgres?client_encoding=utf8")

def carregar_dados_estruturados():
    print("--- INICIANDO CARGA ESTRUTURADA (ETL) ---")


    try:
        print("\n1. Processando Operadoras (Dimensão)...")
        df_full = pd.read_csv("output/dados_enriquecidos.csv", sep=",", encoding="utf-8") 
        
        cols_cadastro = {
            'REGISTRO_ANS': 'registro_ans',
            'CNPJ': 'cnpj',
            'RazaoSocial': 'razao_social',
            'MODALIDADE': 'modalidade',
            'UF': 'uf'
        }
        
        df_ops = df_full.rename(columns=cols_cadastro)
        df_ops = df_ops[cols_cadastro.values()].drop_duplicates(subset=['registro_ans'])
        
        df_ops.to_sql("operadoras_cadastro", con=engine, if_exists="append", index=False)
        print(f"   -> SUCESSO: {len(df_ops)} operadoras cadastradas.")

    except Exception as e:
        print(f"   [ERRO OPERADORAS]: {e}")
        return 


    try:
        print("\n2. Processando Despesas Consolidadas (Fato)...")
        
        df_desp = pd.read_csv("output/consolidado_despesas.csv", sep=",", encoding="utf-8")
        
        df_de_para = pd.read_csv("output/dados_enriquecidos.csv", sep=",", encoding="utf-8")
        df_de_para = df_de_para[['CNPJ', 'REGISTRO_ANS']].drop_duplicates()
        
        df_desp['CNPJ'] = df_desp['CNPJ'].astype(str)
        df_de_para['CNPJ'] = df_de_para['CNPJ'].astype(str)

        print("   -> Cruzando tabelas para encontrar o Registro ANS...")
        df_final = pd.merge(df_desp, df_de_para, on='CNPJ', how='inner')
        
        cols_banco = {
            'REGISTRO_ANS': 'registro_ans',
            'Ano': 'ano',
            'Trimestre': 'trimestre',
            'ValorDespesas': 'valor_despesas'
        }
        
        df_fato = df_final.rename(columns=cols_banco)
        df_fato = df_fato[['registro_ans', 'ano', 'trimestre', 'valor_despesas']]

        df_fato.to_sql("despesas_consolidadas", con=engine, if_exists="append", index=False)
        print(f"   -> SUCESSO: {len(df_fato)} despesas lançadas com ID correto.")

    except Exception as e:
        print(f"   [ERRO DESPESAS]: {e}")


    try:
        print("\n3. Processando Tabela de Analytics...")
        # 4. CORREÇÃO DE ENCODING
        df_agg = pd.read_csv("output/despesas_agregadas.csv", sep=";", encoding="utf-8")
        
        df_agg = df_agg.rename(columns={
            'RazaoSocial': 'razao_social',
            'REGISTRO_ANS': 'registro_ans',
            'UF': 'uf',
            'Total_Despesas': 'total_despesas',
            'Media_Trimestral': 'media_trimestral',
            'Variabilidade_Std': 'variabilidade_std'
        })
        
        df_agg.to_sql("despesas_agregadas_bi", con=engine, if_exists="append", index=False)
        print(f"   -> SUCESSO: {len(df_agg)} registros de BI carregados.")

    except Exception as e:
        print(f"   [ERRO ANALYTICS]: {e}")

if __name__ == "__main__":
    carregar_dados_estruturados()