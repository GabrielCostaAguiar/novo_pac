# Novo PAC — ETL + BI Gerencial

![ETL](https://img.shields.io/badge/ETL-stable-brightgreen)
![BI](https://img.shields.io/badge/BI-em%20desenvolvimento-yellow)

Pipeline de processamento de dados do [Transferegov](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados) para alimentar um **BI gerencial** de monitoramento de propostas e convênios do **Novo PAC** no estado de **Minas Gerais**.

## Visão geral

```
Transferegov (download direto) → raw/ (CSVs) → ETL Python → data/ (CSVs + Excel) → Power BI
```

O pipeline baixa os dados brutos direto do Transferegov, descompacta em `raw/`, filtra por UF, natureza jurídica e programas do PAC, e exporta os resultados em `data/` para alimentar o painel gerencial em Power BI.

## Estrutura do projeto

```
novo_pac/
├── config.py         # Constantes: caminhos, URLs, filtros, listas de programas
├── extract.py        # Download e descompactação dos arquivos do Transferegov
├── load.py           # Carregamento dos CSVs
├── treatment.py      # Funções de limpeza e filtragem
├── logger.py         # Configuração do log
├── main.py           # Orquestração do pipeline
├── BI/
│   └── gestao_novo_pac.pbix  # Painel Power BI
├── raw/              # Dados brutos baixados automaticamente pelo pipeline
├── data/             # Outputs gerados (CSVs tratados, Excel + pipeline.log)
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Instalar dependências:

```bash
pip install -r requirements.txt
```

## Como executar

```bash
python main.py
```

O pipeline executa automaticamente as seguintes etapas:

1. **Extração** — baixa os arquivos `.zip` do Transferegov e descompacta em `raw/`
2. **Carregamento** — lê os CSVs de `raw/`
3. **Tratamento** — aplica filtros e limpeza
4. **Exportação** — salva os resultados em `data/`

### Outputs gerados em `data/`

| Arquivo | Descrição |
|---|---|
| `propostas_tratadas.csv` | Propostas filtradas e limpas |
| `programas_tratados.csv` | Programas filtrados e limpos |
| `ids_tratados.csv` | Relacionamento programa × proposta tratado |
| `convenios_tratados.csv` | Convênios tratados (base principal do BI) |
| `convenios_tratados.xlsx` | Convênios tratados em Excel (input do Power BI) |
| `pipeline.log` | Log de execução completo |

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
