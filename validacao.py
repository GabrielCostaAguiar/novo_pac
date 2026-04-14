'''
Arquivo destinado a validar os dados da UNIÃO com os dados da planilha de controle interno
'''
import pandas as pd
from main import exportar_dados
from config import SAIDA, RAW_DIR

def carregar_dados_csv(caminho, nome='df', sheet_name=None):
    try:
        caminho = str(caminho)
        if caminho.endswith('.xlsx'):
            df = pd.read_excel(caminho, sheet_name=sheet_name)
        else:
            df = pd.read_csv(caminho, encoding='utf-8-sig', sep=';')
        print(f"DataFrame {nome} carregado!")
        return df
    except Exception as erro:
        raise RuntimeError(f"Erro ao carregar {nome}: {erro}") from erro

def tratar_propostas(df, df2):
    try:
        mask = df['NR_PROPOSTA'].isin(df2['Número da Proposta'])
        mantidos = df[mask].reset_index(drop=True)
        nao_mantidos = df[~mask].reset_index(drop=True)

        mantidos = mantidos[mantidos['ANO_DISPONIBILIZACAO'] > 2018].reset_index(drop=True)

        print(f"Registros mantidos: {len(mantidos)} | Não mantidos: {len(nao_mantidos)}")
        return mantidos, nao_mantidos
    except Exception as erro:
        print(f"Erro ao tratar propostas: {erro}")
        raise RuntimeError(f"Erro ao tratar propostas: {erro}") from erro

def tratar_controle(df):
    try:
        # Remove zeros à esquerda do número da proposta (ex: "01744/2024" → "1744/2024")
        df['Número da Proposta'] = df['Número da Proposta'].str.replace(r'^0+', '', regex=True)
        print("Zeros à esquerda removidos da coluna 'Número da Proposta'!")
        return df
    except Exception as erro:
        raise RuntimeError(f"Erro ao tratar controle: {erro}") from erro


if __name__ == "__main__":

    propostas = carregar_dados_csv(SAIDA / 'propostas_filtradas.xlsx', 'Propostas', 'Sheet1')
    convenios = carregar_dados_csv(SAIDA / 'convenios_tratados.xlsx', 'Convênios')
    controle = carregar_dados_csv(RAW_DIR / 'Controle de Propostas - Novo PAC (1ª e 2ª etapa).xlsx', 'Controle', 'NOVO PAC-2023a2025')

    print(propostas.info())
    controle_tratado = tratar_controle(controle)
    print(controle_tratado.info())
    mantidos, nao_mantidos = tratar_propostas(propostas, controle_tratado)

    exportar_dados(mantidos, 'validacao_mantidos')
    exportar_dados(nao_mantidos, 'validacao_nao_mantidos')
