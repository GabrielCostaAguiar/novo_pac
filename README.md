# Novo PAC — ETL + BI Gerencial

![ETL](https://img.shields.io/badge/ETL-stable-brightgreen)
![BI](https://img.shields.io/badge/BI-em%20desenvolvimento-yellow)

Pipeline de processamento de dados do [Transferegov](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados) para alimentar um **BI gerencial** de monitoramento de propostas e convênios do **Novo PAC** no estado de **Minas Gerais**.

## Visão geral

```
Transferegov (CSVs) → ETL Python → convenios_tratados.xlsx → Power BI
```

O pipeline extrai os dados brutos do Transferegov, filtra por UF, natureza jurídica e programas do PAC, e exporta um arquivo `.xlsx` que alimenta o painel gerencial desenvolvido em Power BI (`BI/gestao_novo_pac.pbix`).

## Estrutura do projeto

```
novo_pac/
├── config.py         # Constantes: caminhos, filtros, listas de programas
├── load.py           # Carregamento dos CSVs
├── treatment.py      # Funções de limpeza e filtragem
├── logger.py         # Configuração do log
├── main.py           # Orquestração do pipeline
├── BI/
│   └── gestao_novo_pac.pbix  # Painel Power BI
├── raw/              # Dados brutos de entrada (CSVs do Transferegov)
├── data/             # Outputs gerados (Excel + pipeline.log)
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Instalar dependências:

```bash
pip install -r requirements.txt
```

## Dados de entrada

Baixe os arquivos CSV no portal do [Transferegov](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados) e coloque-os na pasta `raw/`:

| Arquivo | Descrição |
|---|---|
| `siconv_programa.csv` | Cadastro de programas |
| `siconv_proposta.csv` | Propostas apresentadas |
| `siconv_programa_proposta.csv` | Relacionamento programa × proposta |
| `siconv_convenio.csv` | Convênios firmados |

## Como executar

```bash
python main.py
```

O resultado será gerado em `data/convenios_tratados.xlsx`.
O log de execução fica em `data/pipeline.log`.

## BI Gerencial _(em desenvolvimento)_

> **Aviso:** o painel está em desenvolvimento ativo. Funcionalidades e layout podem mudar.

O arquivo `BI/gestao_novo_pac.pbix` contém o painel Power BI conectado ao output do pipeline.

Para atualizar o painel:
1. Execute `python main.py`
2. Abra o arquivo `.pbix` no Power BI Desktop
3. Clique em **Atualizar**

## Filtros aplicados

- **UF:** Minas Gerais (MG)
- **Natureza jurídica:** Administração Pública Estadual, Empresa pública/SEM, EMMAG
- **Programas:** Eixos do Novo PAC (saneamento, saúde, educação, mobilidade urbana, entre outros)
