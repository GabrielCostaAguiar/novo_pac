"""
config.py
---------
Centraliza todas as constantes, parâmetros de filtro e configurações
do pipeline de processamento de propostas SICONV.
"""

from pathlib import Path
from datetime import date
import re

# ── Data atual ────────────────────────────────────────────────────────────
TODAY = date.today()

# ── Diretório raiz do projeto ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
# ── Caminhos dos arquivos ──────────────────────────────────────────────────
# raw/ → dados brutos de entrada (SICONV)
# data/ → arquivos gerados pelo pipeline (resultado, cache de token)
SICONV_PROGRAMAS = BASE_DIR / "raw" / "siconv_programa.csv"
SICONV_PROPOSTAS = BASE_DIR / "raw" / "siconv_proposta.csv"
SICONV_ID = BASE_DIR / "raw" / "siconv_programa_proposta.csv" #Base de dados com os IFs dos programas e propostas apresentadas
SICONV_CONVENIOS = BASE_DIR / "raw" / "siconv_convenio.csv"

SAIDA = BASE_DIR / "data"


#Caminhos para a extração dos arquivos direto do site do Transferegov
PROPOSTAS = 'http://repositorio.dados.gov.br/seges/detru/siconv_proposta.csv.zip'
PROGRAMAS = 'http://repositorio.dados.gov.br/seges/detru/siconv_programa.csv.zip'
ID = 'http://repositorio.dados.gov.br/seges/detru/siconv_programa_proposta.csv.zip'
CONVENIOS = 'http://repositorio.dados.gov.br/seges/detru/siconv_convenio.csv.zip'

#Dicionário com todos os eixos do PAC
NOVO_PAC = {
    "Novo PAC": "Programa de Aceleração do Crescimento",
    "Abastecimento de Água - Urbano": "Água para Todos",
    "Abastecimento de Água - Rural": "Água para Todos",
    "Esgotamento Sanitário - Urbano": "Cidades Sustentáveis e Resilientes",
    "Mobilidade Urbana - Grandes e Médias Cidades": "Cidades Sustentáveis e Resilientes",
    "Periferia Viva - Urbanização de Favelas": "Cidades Sustentáveis e Resilientes",
    "Prevenção a Desastres Naturais: Drenagem Urbana": "Cidades Sustentáveis e Resilientes",
    "Prevenção a Desastres Naturais: Contenção de Encostas": "Cidades Sustentáveis e Resilientes",
    "Regularização Fundiária": "Cidades Sustentáveis e Resilientes",
    "Renovação de Frota": "Cidades Sustentáveis e Resilientes",
    "Resíduos Sólidos": "Cidades Sustentáveis e Resilientes",
    "Minha Casa, Minha Vida": "Cidades Sustentáveis e Resilientes",
    "Novas Ambulâncias – SAMU": "Saúde",
    "Centrais de Regulação – Ambulâncias do SAMU": "Saúde",
    "Centros de Atenção Psicossocial": "Saúde",
    "Centros de Atenção Psicossocial (CAPS)": "Saúde",
    "Centros Especializados em Reabilitação (CER)": "Saúde",
    "Centros de Parto Normal": "Saúde",
    "Maternidades": "Saúde",
    "Policlínicas": "Saúde",
    "Oficinas Ortopédicas": "Saúde",
    "Unidades Básicas de Saúde": "Saúde",
    "Unidades Básicas de Saúde (UBS)": "Saúde",
    "Unidades Odontológicas Móveis": "Saúde",
    "Renovação de Frota - Ambulâncias SAMU": "Saúde",
    "Combo de equipamentos para UBS": "Saúde",
    "Kit de Equipamentos de Teleconsulta": "Saúde",
    "Creches e Escolas de Educação Infantil": "Educação, Ciência e Tecnologia",
    "Escolas em Tempo Integral": "Educação, Ciência e Tecnologia",
    "Transporte Escolar": "Educação, Ciência e Tecnologia",
    "CONVIVE - Centro Comunitário pela Vida": "Infraestrutura Social Inclusiva",
    "CEUs da Cultura": "Infraestrutura Social Inclusiva",
    "Espaços Esportivos Comunitários": "Infraestrutura Social Inclusiva",
    "Centros Esportivos Comunitários": "Infraestrutura Social Inclusiva",
    "Patrimônio Histórico - Projetos de engenharia": "Infraestrutura Social Inclusiva",
}

#COLUNAS A EXCLUI
PROPOSTAS_COLUNAS_EXCLUIR = ['MUNIC_PROPONENTE', 'COD_MUNIC_IBGE', 'DIA_PROP', 'MES_PROP', 'ANO_PROP', 'ENDERECO_PROPONENTE', 'NM_PROPONENTE', 'BAIRRO_PROPONENTE', 'CEP_PROPONENTE', 'NM_BANCO',
                            'SITUACAO_CONTA', 'CD_AGENCIA', 'CD_CONTA']
PROGRAMAS_COLUNAS_EXCLUIR = ['COD_ORGAO_SUP_PROGRAMA', 'DT_PROG_INI_RECEB_PROP', 'DT_PROG_FIM_RECEB_PROP', 'DT_PROG_INI_EMENDA_PAR', 'DT_PROG_INI_BENEF_ESP', 'DT_PROG_FIM_BENEF_ESP','DT_PROG_FIM_EMENDA_PAR',
                             ]


# ── Naturezas jurídicas monitoradas ───────────────────────────────────────
NATUREZAS_JURIDICAS = [
    "Administração Pública Estadual ou do Distrito Federal",
    "Empresa pública/Sociedade de economia mista",
    "EMMAG EMPRESA MUNICIPAL DE MECANIZACAO AGRICOLA",
]

# para afunção de limpar chars do excel
ILLEGAL_CHARS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')