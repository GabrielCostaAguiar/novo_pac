"""
Arquivo destinado a executar o programa e exportar os dados
"""

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

def export_ids(ids, nome_arquivo):
    ids.to_excel(SAIDA / f"{nome_arquivo}.xlsx", index=False)
    logger.info(f"{nome_arquivo} exportado em excel com sucesso!")

if __name__ == "__main__":
    logger.info("=== Iniciando pipeline ===")

    programas = carregar_dados_csv(SICONV_PROGRAMAS, 'Programas')
    propostas = carregar_dados_csv(SICONV_PROPOSTAS, 'Propostas')
    ids = carregar_dados_csv(SICONV_ID, 'IDs')
    convenios = carregar_dados_csv(SICONV_CONVENIOS, 'Convênios')

    propostas_tratadas = tratar_propostas(propostas, PROPOSTAS_COLUNAS_EXCLUIR)
    programas_tratados = tratar_programas(programas, PROGRAMAS_COLUNAS_EXCLUIR)
    ids_tratados = tratar_ids(ids, programas_tratados)
    convenios_tratados = tratar_convenios(convenios, ids_tratados)
    # exibir_dados(convenios, nome='Convênios')

    exportar_dados(convenios_tratados, 'convenios_tratados')
    # export_ids(ids_tratados)

    logger.info("=== Pipeline concluído com sucesso ===")
