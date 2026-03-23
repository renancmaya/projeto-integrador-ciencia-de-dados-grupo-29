# Projeto integrador: Ciência de dados [Grupo 29]
## Integrantes
- Carlos Matheus Lima Coelho
- Diogo Nascimento dos Santos
- Miguel Vieira da Silva
- Renan Cardoso Maia Santos

## Tema do projeto
Análise do Mercado Global de Videogames (1980-2024): Tendências de Vendas, Gêneros e Recepção Crítica

## Objetivo da análise
Compreender a evolução do mercado de jogos eletrônicos ao longo de mais de quatro décadas. O foco é identificar quais gêneros e consoles foram mais rentáveis, analisar a preferência de consumo por região (América do Norte, Japão, Europa/África) e investigar se existe uma correlação direta entre a nota da crítica especializada e o sucesso comercial de um jogo

## Planejamento das tarefas
- **Tarefa 01 [Renan]:** Configuração do repositório no GitHub, estruturação inicial do README e download/validação da base de dados do Kaggle
- **Tarefa 02 [Nome]:** Processo de ETL com Pandas (tratamento de valores nulos em critic_score, total_sales e release date, conversão da coluna release_date para o formato datetime e padronização de textos das colunas genre, console, publisher e developer visando evitar inconsistências em valores que deveriam ser iguais)
- **Tarefa 03 [Nome]:** Análise Exploratória de Dados (EDA), criação de estatísticas descritivas e identificação de outliers (jogos com vendas muito fora do padrão)
- **Tarefa 04 [Nome]:** Desenvolvimento da interface do Dashboard utilizando Streamlit e integração das lógicas de filtragem
- **Tarefa 05 [Nome]:** Criação dos gráficos finais, testes de usabilidade do dashboard, documentação final e preparação para a apresentação

## Tecnologias
- **Python:** Linguagem principal do projeto, responsável por integrar todas as bibliotecas e a lógica de funcionamento.
- **Pandas:** Utilizado para manipulação, limpeza (ETL) e estruturação dos dados que alimentarão o dashboard.
- **Matplotlib / Seaborn:** Bibliotecas utilizadas para a criação de gráficos estáticos e análises visuais rápidas durante a fase de Análise Exploratória de Dados (EDA).
- **Plotly:** Responsável pela criação de gráficos interativos e dinâmicos a partir dos dados processados pelo Pandas para a interface final.
- **Google Colab / Jupyter Notebook:** Ambiente interativo utilizado para testes preliminares, trabalho colaborativo da equipe e documentação da EDA.
- **Streamlit:** Framework responsável por criar a interface web do dashboard, integrando os filtros interativos com o Pandas e exibindo as visualizações do Plotly.

## Métricas principais
### Vendas e Faturamento
- **Vendas globais totais:** soma da coluna `total_sales`
- **Média de vendas por jogo:** média geral da coluna `total_sales`
- **Recorde histórico de vendas:** o maior valor numérico da coluna `total_sales`
- **Título mais vendido de todos os tempos:** nome do jogo com o maior valor em `total_sales`
- **Market share regional:** percentual das vendas globais que cada região representa: `na_sales`, `jp_sales`, etc
### Recepção e Crítica
- **Média da nota da crítica:** média geral da coluna `critic_score`
- **Total de jogos aclamados:** contagem de jogos com `critic_score` > 9
- **Título mais aclamado de todos os tempos:** nome do jogo com o maior valor em `critic_score`
- **Total de fracassos:** contagem de jogos com `critic_score` < 4
### Indústria e Mercado
- **Total de jogos lançados no período:** contagem da coluna `title`
- **Total de consoles ativos:** contagem de valores únicos da coluna `console`
- **Total de publicadoras:** contagem de valores únicos da coluna `publisher`
- **Gênero mais rentável:** nome do gênero com maior soma de `total_sales`
- **Gênero mais aclamado:** nome do gênero com a maior quantidade de jogos com `critic_score` > 9
- **Publicadora mais rentável:** nome da publicadora com maior soma de `total_sales`
- **Publicadora mais aclamada:** nome da publicadora com a maior quantidade de jogos com `critic_score` > 9
- **Console mais rentável:** nome do console com maior soma de `total_sales`
- **Console com mais títulos aclamados:** nome do console com a maior quantidade de jogos com `critic_score` > 9

## Ideia inicial de dashboard
- **Filtros Interativos:** Seletores de período (anos), região, gênero e console para recalcular os dados dinamicamente (Elementos de Interface)
- **Cards de Métricas:** Exibição dos KPIs em destaque de Vendas, Crítica e Indústria (Cards Numéricos)
- **Evolução Geral:** Vendas globais ao longo dos anos (Gráfico de Linha)
- **Comparativo de Ciclo de Vida:** Vendas por Console ao longo do tempo (Gráfico de Linha)
- **Tendências de Consumo:** Vendas por Gênero ao longo do tempo (Gráfico de Linha)
- **Top 10 Publicadoras:** Ranking de volume de vendas (Gráfico de Barras Horizontais)
- **Top 10 Gêneros:** Ranking de volume de vendas (Gráfico de Barras Horizontais)
- **Top 10 Consoles:** Ranking de volume de vendas (Gráfico de Barras Horizontais)
- **Market Share de Gêneros:** Quais categorias dominam qual fatia do mercado (Gráfico de Pizza)
- **Relação Crítica vs Vendas:** Nota da crítica (`critic_score`) no eixo Y e vendas globais (`total_sales`) no eixo X (Gráfico de Dispersão)
- **Distribuição Regional:** Percentual das vendas por região (`na_sales`, `jp_sales`, `pal_sales`, `other_sales`) (Gráfico de Pizza)
