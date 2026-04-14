import re
import pandas as pd

from config import NOVO_PAC, NATUREZAS_JURIDICAS, ILLEGAL_CHARS_RE
from logger import logger

def tratar_propostas(df, colunas_excluir, uf='MG', renomear=None):
    try:
        # Filtrando por UF
        df = df[df['UF_PROPONENTE'] == uf].copy()
        logger.info(f"DataFrame de propostas filtrado por UF = {uf}!")
        # Filtrando natureza jurídica
        df = df[df['NATUREZA_JURIDICA'].isin(NATUREZAS_JURIDICAS)].copy()
        logger.info("DataFrame de propostas filtrado por natureza jurídica!")
        # Excluindo colunas desnecessárias
        df = df.drop(columns=colunas_excluir)
        logger.info("Colunas desnecessárias excluídas do DataFrame de propostas!")
        if renomear is not None:
            df = df.rename(columns=renomear)
            logger.info("Colunas do DataFrame de propostas renomeadas com sucesso!")

        return df

    except Exception as erro:
        # Relança o erro com contexto claro, evitando retorno silencioso de None
        logger.error(f"Erro ao tratar propostas: {erro}")
        raise RuntimeError(f"Erro ao tratar propostas: {erro}") from erro

def tratar_programas(programas, colunas_excluir, uf='MG'):
    try:
        # Excluindo colunas desnecessárias
        programas = programas.drop(columns=colunas_excluir)
        logger.info("Colunas desnecessárias excluídas do DataFrame de programas!")
        # Filtrando natureza jurídica
        programas = programas[programas['NATUREZA_JURIDICA_PROGRAMA'].isin(NATUREZAS_JURIDICAS)].copy()
        logger.info("DataFrame de programas filtrado por natureza jurídica!")
        programas = programas[programas['SIT_PROGRAMA'] != 'INATIVO'].copy()
        logger.info("DataFrame de programas filtrado por situação (removidos INATIVO)!")
        programas = programas[programas['UF_PROGRAMA'] == uf].copy()
        logger.info(f"DataFrame de programas filtrado por UF = {uf}!")

        # Filtrando por nome dos programas do PAC (busca parcial, sem exigir correspondência exata)
        padrao = "|".join(re.escape(termo) for termo in NOVO_PAC.keys())
        mask = programas['NOME_PROGRAMA'].str.contains(padrao, case=False, na=False)
        logger.info("DataFrame filtrado pelo nome dos programas do PAC!")

        return programas[mask].reset_index(drop=True)

    except Exception as error:
        logger.error(f"Erro ao tratar programas: {error}")
        raise RuntimeError(f"Erro ao tratar programas: {error}") from error

def tratar_ids(ids, programas_tratados, propostas_tratadas):
    try:
        ids_validos = programas_tratados['ID_PROGRAMA'].unique()
        ids_filtrados = ids[ids['ID_PROGRAMA'].isin(ids_validos)].reset_index(drop=True)
        ids_filtrados_propostas = ids_filtrados[ids_filtrados['ID_PROPOSTA'].isin(propostas_tratadas['ID_PROPOSTA'])].reset_index(drop=True)
        
        logger.info(f"IDs tratados: {len(ids_filtrados_propostas)} registros mantidos!")

        return ids_filtrados_propostas

    except Exception as error:
        logger.error(f"Erro ao tratar IDs: {error}")
        raise RuntimeError(f"Erro ao tratar IDs: {error}") from error

def tratar_convenios(df, df_id):
    """
    Função que trata a base de dados de convênios do siconv,
    utilizando ID_PROPOSTA de acordo com os programas do PAC
    """
    try:
        df = df[df['ID_PROPOSTA'].isin(df_id['ID_PROPOSTA'])].reset_index(drop=True)
        logger.info(f"Convênios filtrados: {len(df)} registros mantidos.")

        return df

    except Exception as error:
        logger.error(f"Erro ao tratar convênios: {error}")
        raise RuntimeError(f"Erro ao tratar convênios: {error}") from error

def _limpar_chars_ilegais(df):
    return df.apply(lambda col: col.map(
        lambda x: ILLEGAL_CHARS_RE.sub('', x) if isinstance(x, str) else x
    ))

def consolidar_dados(propostas, ids, programas):
    try:
        colunas_programas = ['ID_PROGRAMA', 'NOME_PROGRAMA', 'SIT_PROGRAMA', 'ANO_DISPONIBILIZACAO',
                             'NOME_SUBTIPO_PROGRAMA', 'DESCRICAO_SUBTIPO_PROGRAMA']

        # ids já filtrados guiam a consolidação; propostas e programas entram via merge
        df_consolidado = (
            ids[['ID_PROPOSTA', 'ID_PROGRAMA']]
            .merge(propostas, on='ID_PROPOSTA', how='inner')
            .merge(programas[colunas_programas], on='ID_PROGRAMA', how='inner')
            .query('ANO_DISPONIBILIZACAO > 2018')
            .reset_index(drop=True)
        )

        logger.info(f"Dados consolidados com sucesso: {len(df_consolidado)} registros.")
        return df_consolidado
    except Exception as error:
        logger.error(f"Erro ao consolidar dados: {error}")
        raise RuntimeError(f"Erro ao consolidar dados: {error}") from error
