# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Insight Vinhedo

## Grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/renatoruizcai">Renato Ruiz Cai</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>


## 📜 Descrição

*Este projeto foi desenvolvido como parte de uma aplicação voltada à Agricultura Digital, com o objetivo de auxiliar no planejamento agrícola por meio de cálculos de área de plantio, manejo de insumos e análise estatística, integrando Python e R em uma solução única.
A aplicação simula um cenário real de uso em uma fazenda localizada na região de Vinhedo (SP), contemplando duas culturas relevantes: uva (viticultura) e milho (lavoura extensiva).*


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>data</b>: Pasta responsável por armazenar os dados gerados pela aplicação. Contém o arquivo <code>agricultural_data.csv</code>, que é exportado pelo sistema em Python e utilizado pelo R para análise estatística.

- <b>scripts</b>: Contém os scripts desenvolvidos em R.
   - <code>agricultural_statistics.R</code>: realiza cálculos estatísticos (média e desvio padrão) com base nos dados exportados.
   - <code>weather_report.R</code>: consome a API pública open-meteo para obter dados climáticos em tempo real e exibi-los no terminal.

- <b>src</b>: Contém todo o código fonte da aplicação em Python, organizado de forma modular:
   - <code>main.py</code>: ponto de entrada da aplicação e controle do fluxo do sistema via menu interativo.
   - <code>menu.py</code>: responsável pela exibição e captura das opções do menu no terminal.
   - <code>crop_data.py</code>: coleta e valida os dados inseridos pelo usuário, além de integrar os cálculos de área e insumo.
   - <code>data_store.py</code>: gerencia o armazenamento dos dados em memória (vetor) e implementa as operações de CRUD.
   - <code>area_calculations.py</code>: contém as funções responsáveis pelos cálculos de área e estrutura de plantio.
   - <code>input_calculations.py</code>: realiza os cálculos de insumos com base na cultura selecionada.
   - <code>export_data.py</code>: exporta os dados armazenados para o arquivo CSV utilizado pelo R.
   - <code>run_r_script.py</code>: executa o script de estatísticas em R a partir do Python.
   - <code>run_weather_script.py</code>: executa o script de clima em R e retorna as informações ao terminal.
   - <code>constants.py</code>: centraliza constantes do sistema, como mensagens, índices e opções de menu.

- <b>README.md</b>: Arquivo que apresenta uma visão geral do projeto, incluindo sua finalidade, estrutura e instruções de uso.

## 🔧 Como executar o código

*Pré Requisitos:*

*Git - Utilizado para clonar o repositório do projeto.*

*Visual Studio Code (VS Code) ou outra IDE/editor de sua preferência. Recomenda-se o VS Code para facilitar a execução dos arquivos Python e R.*

*Python 3.10 ou superior - Utilizado no desenvolvimento da aplicação principal.*

*R 4.3 ou superior - Utilizado para processamento estatístico e consulta de dados meteorológicos.*

*Pacote jsonlite no R - Necessário para consumir a API meteorológica pública no arquivo weather_report.R.*


*Fase 1 — Clonar o repositório:*

*No terminal, execute: git clone git@github.com:renatoruiz2607/fiapAgroInsightVinhedo.git*

*Em seguida, acesse a pasta do projeto: cd fiapAgroInsightVinhedo*


*Fase 2 — Preparar o ambiente Python:*

*No terminal, verifique se o Python está instalado: python3 --version*


*Fase 3 — Preparar o ambiente R:*

*No terminal, verifique se o R está instalado: R --version*


*Fase 4 — Executar a aplicação Python:*

*Dê play no sistema a partir do arquivo src/main.py*


*Ao iniciar, o sistema exibirá um menu interativo no terminal com opções para:*
   - *adicionar registros de culturas*
   - *listar registros cadastrados*
   - *atualizar registros*
   - *excluir registros*
   - *exportar os dados para CSV*
   - *executar a análise estatística em R*
   - *executar a consulta meteorológica em R*
   - *encerrar a execução*


## 🗃 Histórico de lançamentos

* 1.0.0 - 22/02/2026
    * 
* 0.5.0 - 22/02/2026
    * 
* 0.4.0 - 22/02/2026
    * 
* 0.3.0 - 21/02/2026
    * 
* 0.2.0 - 21/02/2026
    * 
* 0.1.0 - 20/02/2026
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


