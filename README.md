# Dashboard de Analise de Salarios na Area de Dados

Este projeto consiste em uma aplicacao interativa desenvolvida em Python com a biblioteca Streamlit para exploracao de dados salariais do mercado de dados global. O projeto foi desenvolvido com base na Imersao Dados da Alura.

## Funcionalidades

A aplicacao processa dados de um repositorio publico e oferece as seguintes capacidades:

* **Filtros Laterais**: Selecao dinamica por ano, nivel de experiencia, tipo de contrato e porte da empresa.
* **Tratamento de Dados**: Traducao automatica de siglas de senioridade (ex: EN para Junior) e regimes de trabalho.
* **Metricas Principais**: Calculo em tempo real de salario medio, maximo, minimo e contagem de registros filtrados.
* **Visualizacoes**: 
    * Grafico de barras horizontais com o Top 10 cargos por media salarial.
    * Histograma de distribuicao das faixas salariais em USD.
    * Grafico de rosca para proporcao de regimes (Presencial, Hibrido e Remoto).
    * Mapa mundi (choropleth) demonstrando a media salarial de Data Scientists por pais.
* **Exportacao**: Visualizacao da tabela de dados detalhada e geracao de arquivo CSV para download.

## Tecnologias Utilizadas

* **Python**: Linguagem de programacao base.
* **Streamlit**: Interface web e interatividade.
* **Pandas**: Manipulacao e limpeza de dados.
* **
