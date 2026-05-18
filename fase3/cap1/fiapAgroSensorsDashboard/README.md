# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://raw.githubusercontent.com/agodoi/template/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Sensors Dashboard


## 📜 Descrição

*AgroSensorsDashboard é uma aplicação desenvolvida para visualização e análise de dados agrícolas coletados por sensores inteligentes. O projeto apresenta métricas, indicadores e gráficos relacionados a irrigação, umidade do solo, pH, nutrientes e previsão de chuva, auxiliando no monitoramento e na tomada de decisão no agronegócio.*

*A aplicação faz parte do ecossistema AgroSensors e tem como objetivo transformar dados em informações visuais claras, apoiando análises operacionais e preditivas de forma simples e centralizada.*


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>scripts</b>: Contém os arquivos auxiliares utilizados pelo projeto.
   - <code>irrigation_training_data.csv</code>: dataset simulado utilizado como base de dados para análise das informações agrícolas exibidas no dashboard.

- <b>src</b>: Contém o código-fonte principal da aplicação de dashboard:
   - <code>app.py</code>: arquivo principal responsável pela execução do dashboard, carregamento do dataset, tratamento dos dados, cálculo das métricas e exibição dos gráficos analíticos.

- <b>README.md</b>: Arquivo que apresenta uma visão geral do projeto, incluindo sua finalidade, estrutura e instruções de uso.


## 🏗️ Arquitetura

*O projeto foi estruturado de forma simplificada, mantendo toda a lógica principal concentrada em um único arquivo (app.py).*

*Essa abordagem foi adotada por se tratar de uma aplicação de pequeno porte, com foco em rapidez na implementação de novas métricas e gráficos*

*Em projetos maiores, a componentização seria recomendada para melhorar a organização, manutenção e escalabilidade do código.*

*No entanto, para este cenário acadêmico, a separação em múltiplos componentes não traria ganho significativo de desempenho ou redução de memória.*


## 🚀 Próximos passos

*Como evolução futura do projeto, o ideal seria permitir a importação de arquivos CSV diretamente pela interface web do dashboard. Dessa forma, usuários poderiam carregar novos conjuntos de dados dinamicamente, atualizando métricas, gráficos e análises sem necessidade de alterações no código-fonte.*

*Entretanto, por se tratar de um projeto acadêmico com foco demonstrativo, optou-se por manter apenas um dashboard utilizando um dataset simulado já incorporado ao projeto através do arquivo `irrigation_training_data.csv`. Essa abordagem simplifica a arquitetura da aplicação, reduz a complexidade de implementação e garante maior estabilidade para apresentação e execução do projeto.*


## 🔧 Como executar o código

*Pré Requisitos:*

*Git - Utilizado para clonar o repositório do projeto.*

*Visual Studio Code (VS Code)*

*Extensões: streamlit e pandas* 

*Garantir que tenha as instalações necessárias das linguagens C/C++ e Python*


*Fase 1 — Clonar o repositório:*

*No terminal, execute: `git clone git@github.com:renatoruiz2607/fiapCursoTecIA.git`*

*Em seguida, faça o trajeto até a pasta principal:*

*cd fiapCursoTecIA*

*cd fase3*

*cd cap1*

*cd fiapAgroSensorsDashboard*


*Fase 2 — Executar a aplicação*

*Execute o comando: `python3 -m streamlit run src/app.py`*

*O terminal vai exibir algo como: `Local URL: http://localhost:8501` e abrirá a página no navegador automaticamente*

*Caso não aconteça, abra esse endereço no navegador*


*Fase 4 - Funcionamento*

*O sistema permite visualizar em uma página web os indicadores e gráficos relacionados ao dataset 'irrigation_training_data.csv'*


## 📊 Análise dos Dados

### Métricas
*O dashboard apresenta métricas calculadas a partir de uma base simulada com 100 cenários agrícolas relacionados à irrigação da cultura da uva.*

- *Umidade média do solo: **43.37%***

  *A média de umidade permaneceu abaixo do limite crítico de 50%, indicando predominância de cenários em que a irrigação pode ser necessária.*
- *pH médio: **6.07***

  *O valor médio de pH permaneceu dentro da faixa ideal para a cultura da uva, próxima do intervalo utilizado nas regras de decisão do sistema.*
- *Cenários com irrigação: **40***

  *Dos 100 cenários simulados, 40 resultaram em recomendação de irrigação, considerando simultaneamente clima, umidade, nutrientes e modelo estatístico.*
- *Bloqueados por chuva: **10***

  *Em 10 cenários a irrigação foi bloqueada devido à previsão de chuva, seguindo a regra climática baseada na API OpenWeather.*
- *Nutrientes adequados: **85***

  *A maior parte dos cenários apresentou condições nutricionais adequadas, considerando a presença de potássio e pelo menos dois nutrientes ativos.*
  
<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Métricas principais</i>
</p>

### Gráficos
***Distribuição da umidade do solo***

*O gráfico de distribuição da umidade do solo apresenta a variação dos níveis de umidade registrados ao longo das análises agrícolas realizadas.*

*É possível observar três comportamentos principais:*

- *Faixas de baixa umidade (aproximadamente entre **25%** e **45%**), indicando condições em que a irrigação tende a ser necessária para manutenção da cultura.*
- *Faixas de alta umidade (acima de **50%**), representando situações em que o solo já possui quantidade suficiente de água, reduzindo a necessidade de irrigação.*
- *Variações graduais entre os valores, permitindo acompanhar diferentes condições do solo e comportamentos ambientais ao longo das medições.*

*O comportamento apresentado demonstra diferentes condições hídricas do solo, contribuindo para análises mais completas da tomada de decisão da irrigação.*
  
<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Distribuição de umidade de solo</i>
</p>

***Distribuição do pH do solo***

*O gráfico de distribuição do pH do solo apresenta a variação dos níveis de acidez e alcalinidade registrados durante as análises agrícolas.*

*A maior parte dos valores permaneceu próxima da faixa ideal para a cultura da uva, concentrando-se entre aproximadamente **5.5** e **6.5**, intervalo considerado adequado para absorção de nutrientes e desenvolvimento da plantação.*

*Também é possível observar alguns pontos fora da faixa ideal, representando condições mais ácidas ou alcalinas do solo. Nessas situações, o sistema tende a bloquear a irrigação, pois valores inadequados de pH podem comprometer o aproveitamento dos nutrientes pela cultura.*

*O comportamento do gráfico demonstra diferentes condições químicas do solo, permitindo que a lógica de decisão considere cenários mais variados durante a análise da irrigação.*

<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Distribuição do pH do solo</i>
</p>

***Umidade média por decisão de irrigação***

*O gráfico de umidade média por decisão de irrigação apresenta a relação entre os níveis médios de umidade do solo e a decisão final do sistema.*

*Os resultados demonstram que os cenários classificados como “**Irrigar**” possuem média de umidade significativamente menor quando comparados aos cenários classificados como “Não irrigar”.*

*Essa diferença evidencia que a umidade do solo atua como uma das principais variáveis da lógica de decisão, permitindo que o sistema identifique situações em que a cultura necessita de reposição hídrica.*

*Já os cenários classificados como “**Não irrigar**” apresentam níveis médios de umidade mais elevados, indicando condições em que o solo já possui quantidade adequada de água para a plantação.*

<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Umidade média por decisão de irrigação</i>
</p>

***Relação entre pH e umidade por decisão de irrigação***

*O gráfico de relação entre pH e umidade por decisão de irrigação apresenta como essas duas variáveis influenciam simultaneamente a tomada de decisão do sistema.*

*Os pontos classificados como “**Irrigar**” concentram-se majoritariamente em faixas de menor umidade e valores de pH próximos da faixa ideal para a cultura da uva, indicando condições adequadas para acionamento da irrigação.*

*Já os pontos classificados como “**Não irrigar**” aparecem principalmente em situações com maior umidade do solo ou valores de pH fora da faixa considerada ideal, demonstrando que o sistema considera múltiplas variáveis de forma integrada antes de recomendar a irrigação.*

*O comportamento visual do gráfico evidencia a combinação entre condições hídricas e químicas do solo na lógica de decisão implementada no projeto.*

<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Relação entre pH e umidade por decisão de irrigação</i>
</p>

## 🎥 Vídeo demonstrativo

▶️ [Assistir no YouTube](https://www.youtube.com/watch?v=AXcdfUI0DlU)


## 🗃 Histórico de lançamentos

* 1.0.0 - 17/05/2026
    * 
* 0.4.0 - 17/05/2026
    * 
* 0.3.0 - 17/05/2026
    * 
* 0.2.0 - 17/05/2026
    * 
* 0.1.0 - 17/05/2026
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


