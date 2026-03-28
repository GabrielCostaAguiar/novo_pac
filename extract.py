"""
Arquivo destinado a extração das bases de dados direto do site do Transferegov
"""
import zipfile
import requests

from config import (PROPOSTAS,
    PROGRAMAS,
    ID,
    CONVENIOS,
    RAW_DIR
)
from logger import logger

def extracao_df():
    requisicao_conjunta = {
        "PROPOSTAS": PROPOSTAS,
        "PROGRAMAS": PROGRAMAS,
        "ID": ID,
        "CONVENIOS": CONVENIOS,
    }
    RAW_DIR.mkdir(exist_ok=True)
    logger.info("=== Iniciando extração dos arquivos ===")
    try:
        for nome, requisicao in requisicao_conjunta.items():
            logger.info(f"Baixando {nome}...")
            zip_path = RAW_DIR / f"{nome}.zip"
            with requests.get(requisicao, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            logger.info(f"{nome} baixado. Descompactando...")
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(RAW_DIR)
            zip_path.unlink()
            logger.info(f"{nome} descompactado em raw/ com sucesso.")
    except Exception as erro:
        logger.error(f"Erro na extração: {erro}")
        raise
    logger.info("=== Extração concluída com sucesso ===")
