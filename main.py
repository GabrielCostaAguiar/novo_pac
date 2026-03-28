"""
Arquivo destinado a executar o programa e exportar os dados
"""

from extract import extracao_df
from load import carregar_dados_csv

from treatment import (
    tratar_propostas, tratar_programas,
    tratar_ids, tratar_convenios,
    _limpar_chars_ilegais
)

from config import (
    SICONV_PROGRAMAS,
    SICONV_PROPOSTAS,
    SICONV_ID,
    PROPOSTAS_COLUNAS_EXCLUIR,
    PROGRAMAS_COLUNAS_EXCLUIR,
    SAIDA, SICONV_CONVENIOS
)

from logger import logger


def exibir_dados(df, nome='df'):
    print(f"DataFrame em exibição: {nome}")
    print(df.head())
    print(df.info())

def exportar_dados(df, nome_arquivo):
    try:
        df.to_excel(SAIDA / f"{nome_arquivo}.xlsx", index=False)
        logger.info(f"{nome_arquivo} exportado em excel com sucesso!")
    except Exception as _:
        logger.warning(f"Caracteres ilegais detectados em {nome_arquivo}, executando correção...")
        try:
            _limpar_chars_ilegais(df).to_excel(SAIDA / f"{nome_arquivo}.xlsx", index=False)
            logger.info(f"{nome_arquivo} exportado em excel com sucesso após correção!")
        except Exception as erro:
            logger.error(f"Erro ao exportar {nome_arquivo}: {erro}")

def exportar_csv(df, nome_arquivo):
    caminho = SAIDA / f"{nome_arquivo}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8")
    logger.info(f"{nome_arquivo} exportado em CSV em data/ com sucesso!")

def export_ids(ids, nome_arquivo):
    ids.to_excel(SAIDA / f"{nome_arquivo}.xlsx", index=False)
    logger.info(f"{nome_arquivo} exportado em excel com sucesso!")

if __name__ == "__main__":
    logger.info("=== Iniciando pipeline ===")

    extracao_df()

    programas = carregar_dados_csv(SICONV_PROGRAMAS, 'Programas')
    propostas = carregar_dados_csv(SICONV_PROPOSTAS, 'Propostas')
    ids = carregar_dados_csv(SICONV_ID, 'IDs')
    convenios = carregar_dados_csv(SICONV_CONVENIOS, 'Convênios')

    propostas_tratadas = tratar_propostas(propostas, PROPOSTAS_COLUNAS_EXCLUIR)
    programas_tratados = tratar_programas(programas, PROGRAMAS_COLUNAS_EXCLUIR)
    ids_tratados = tratar_ids(ids, programas_tratados)
    convenios_tratados = tratar_convenios(convenios, ids_tratados)
    # exibir_dados(convenios, nome='Convênios')

    exportar_csv(propostas_tratadas, 'propostas_tratadas')
    exportar_csv(programas_tratados, 'programas_tratados')
    exportar_csv(ids_tratados, 'ids_tratados')
    exportar_csv(convenios_tratados, 'convenios_tratados')

    exportar_dados(convenios_tratados, 'convenios_tratados')
    # export_ids(ids_tratados)

    logger.info("=== Pipeline concluído com sucesso ===")
