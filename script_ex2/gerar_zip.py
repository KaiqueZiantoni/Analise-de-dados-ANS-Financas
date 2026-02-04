import zipfile
import logging
from pathlib import Path
from typing import Final

FILE_TO_ZIP: Final[Path] = Path("output/despesas_agregadas.csv")
USER_NAME: Final[str] = "Kaique_Ziantoni" 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TechLead_Entrega")

def executar():
    arquivo_fonte = FILE_TO_ZIP
    nome_usuario = USER_NAME
    zip_name = f"Teste_{nome_usuario.replace(' ', '_')}.zip"
    zip_path = Path("output") / zip_name

    if not arquivo_fonte.exists():
        logger.error(f"Erro: O arquivo {arquivo_fonte} não existe para ser compactado.")
        return

    try:
        logger.info(f"Criando pacote de entrega: {zip_name}...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(arquivo_fonte, arcname=arquivo_fonte.name)
        
        logger.info(f"Processo concluído. Arquivo pronto para envio: {zip_path}")
    
    except Exception as e:
        logger.error(f"Falha na compactação: {e}")

if __name__ == "__main__":
    executar()