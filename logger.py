"""
logger.py
---------
Configura o logger central do projeto.
Grava mensagens tanto no terminal quanto em data/pipeline.log.
"""

import logging
from config import SAIDA

LOG_FILE = SAIDA / "pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # grava em arquivo
        logging.StreamHandler(),                           # exibe no terminal
    ]
)

logger = logging.getLogger(__name__)
