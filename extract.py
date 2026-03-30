"""
Arquivo destinado a extração das bases de dados direto do site do Transferegov
"""
import zipfile
from datetime import date
import requests

from config import (PROPOSTAS,
    PROGRAMAS,
    ID,
    CONVENIOS,
    RAW_DIR,
    SICONV_PROPOSTAS,
    SICONV_PROGRAMAS,
    SICONV_ID,
    SICONV_CONVENIOS,
    TODAY,
)
from logger import logger

def extracao_df():
    requisicao_conjunta = {
        "PROPOSTAS": PROPOSTAS,
        "PROGRAMAS": PROGRAMAS,
        "ID": ID,
        "CONVENIOS": CONVENIOS,
    }
    arquivos_raw = [SICONV_PROPOSTAS, SICONV_PROGRAMAS, SICONV_ID, SICONV_CONVENIOS]
    todos_atuais = all(
        f.exists() and date.fromtimestamp(f.stat().st_mtime) == TODAY
        for f in arquivos_raw
    )
    if todos_atuais:
        logger.info("Arquivos já atualizados hoje. Download ignorado.")
        return

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
