import pandas as pd
import logging
from pathlib import Path
from typing import Final

INPUT_PATH: Final[Path] = Path("output/dados_enriquecidos.csv")
OUTPUT_CSV: Final[Path] = Path("output/despesas_agregadas.csv")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TechLead_Agregacao")

def executar() :
    input_file = INPUT_PATH
    if not input_file.exists():
        logger.error(f"Arquivo não encontrado: {input_file}")
        raise FileNotFoundError

    logger.info("Lendo base enriquecida...")
    df = pd.read_csv(input_file)

    logger.info("Iniciando cálculos de agregação e variabilidade...")
    df_agregado = df.groupby(['RazaoSocial', 'REGISTRO_ANS', 'UF']).agg(
        Total_Despesas=pd.NamedAgg(column='ValorDespesas', aggfunc='sum'),
        Media_Trimestral=pd.NamedAgg(column='ValorDespesas', aggfunc='mean'),
        Variabilidade_Std=pd.NamedAgg(column='ValorDespesas', aggfunc='std')
    ).reset_index()

    df_agregado['Variabilidade_Std'] = df_agregado['Variabilidade_Std'].fillna(0)

    df_ordenado = df_agregado.sort_values(by='Total_Despesas', ascending=False)

    df_ordenado.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig', sep=';')
    logger.info(f"Arquivo salvo com sucesso em: {OUTPUT_CSV}")
    
    return df_ordenado

if __name__ == "__main__":
    df_final = executar()
    print(df_final.head())