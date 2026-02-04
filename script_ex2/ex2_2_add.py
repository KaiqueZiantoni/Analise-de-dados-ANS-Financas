import pandas as pd
import logging
from pathlib import Path
from typing import Optional, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent # Sobe dois níveis se estiver em subpasta
DATA_DIR = BASE_DIR / "Registros_Ativos"
OUTPUT_DIR = BASE_DIR / "output"

def carregar_dados(caminho: Path, separador: str = ',', encoding: str = 'utf-8-sig') -> pd.DataFrame:
    try:
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        
        return pd.read_csv(caminho, sep=separador, encoding=encoding, dtype={'CNPJ': str})
    except Exception as e:
        logger.error(f"Falha ao ler {caminho}: {e}")
        raise

def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas para UPPERCASE e SNAKE_CASE."""
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
    return df

def enriquecer_dados():
    logger.info("Iniciando Pipeline de Enriquecimento (Etapa 2.2)...")
    
    file_despesas = OUTPUT_DIR / 'consolidado_despesas.csv'
    file_cadop = DATA_DIR / 'operadoras_ativas.csv'
    
    try:
        df_despesas = carregar_dados(file_despesas)
        df_cadop = carregar_dados(file_cadop, separador=';', encoding='iso-8859-1')
    except Exception:
        return 

    df_cadop = normalizar_colunas(df_cadop)
    logger.info(f"Colunas detectadas no cadastro: {df_cadop.columns.tolist()[:5]}...")

    col_registro_alvo = 'REGISTRO_OPERADORA'
    if col_registro_alvo not in df_cadop.columns:
        logger.error(f"Coluna {col_registro_alvo} não encontrada no cadastro. Colunas disponíveis: {df_cadop.columns}")
        return

    logger.info("Aplicando regra de unicidade (1:1) no cadastro...")
    df_cadop_clean = df_cadop.drop_duplicates(subset=['CNPJ'], keep='last')

    logger.info("Realizando Left Join...")
    colunas_interesse = ['CNPJ', col_registro_alvo, 'MODALIDADE', 'UF']
    
    missing_cols = [c for c in colunas_interesse if c not in df_cadop_clean.columns]
    if missing_cols:
        logger.error(f"Colunas faltando no cadastro para o join: {missing_cols}")
        return

    df_final = pd.merge(
        df_despesas,
        df_cadop_clean[colunas_interesse],
        on='CNPJ',
        how='left'
    )

    df_final.rename(columns={col_registro_alvo: 'REGISTRO_ANS'}, inplace=True)

    mask_match = ~df_final['REGISTRO_ANS'].isna()
    df_enriquecidos = df_final[mask_match]
    df_quarentena = df_final[~mask_match]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    path_ok = OUTPUT_DIR / 'dados_enriquecidos.csv'
    path_bad = OUTPUT_DIR / 'quarentena_cadastral.csv'

    df_enriquecidos.to_csv(path_ok, index=False, encoding='utf-8-sig')
    df_quarentena.to_csv(path_bad, index=False, encoding='utf-8-sig')

    logger.info("-" * 30)
    logger.info(f"PIPELINE CONCLUÍDO COM SUCESSO")
    logger.info(f"Registros Validados: {len(df_enriquecidos)}")
    logger.info(f"Registros Quarentena: {len(df_quarentena)}")
    logger.info(f"Output gerado em: {path_ok}")

if __name__ == "__main__":
    enriquecer_dados()