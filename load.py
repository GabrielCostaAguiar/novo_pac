import pandas as pd
"""
Arquivo destinado ao load dos dados do projeto
"""
def carregar_dados_csv(df, nome='df'):
    try:
        # Carregar os dados dos arquivos CSV
        df = pd.read_csv(df, encoding='utf-8-sig', sep=';')
        print(f"DataFrame {nome} carregado!")

        return df
    except Exception as erro:
        print(f"Erro ao tentar carregar o DataFrame: {erro}")