# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://raw.githubusercontent.com/agodoi/template/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Sensors Intelligence

## Grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/renatoruizcai">Renato Ruiz Cai</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>


## 📜 Descrição

*O AgroSensorsIntelligence é um protótipo de Assistente Agrícola Inteligente desenvolvido para transformar dados agrícolas em informações estratégicas para apoio à tomada de decisão no campo.*

*A solução realiza o monitoramento de variáveis críticas da lavoura, como umidade do solo, pH, nível de nutrientes, luminosidade, temperatura e umidade do ar, permitindo o acompanhamento contínuo das condições de cultivo.*

*Com base no histórico de dados coletados, o sistema gera previsões sobre indicadores agrícolas relevantes, incluindo umidade do solo, pH, nível de nutrientes, produtividade esperada e necessidade de irrigação. A partir dessas previsões, são apresentadas recomendações de irrigação e manejo agrícola, auxiliando na identificação de ações que podem contribuir para melhores condições de cultivo.*

*O projeto também disponibiliza uma visão analítica dos dados, permitindo acompanhar métricas de desempenho dos modelos preditivos, identificar correlações entre variáveis agrícolas, visualizar tendências de produtividade e interpretar os resultados das previsões de forma simples e acessível.*

*O objetivo da solução é demonstrar como dados agrícolas podem ser utilizados para apoiar decisões mais inteligentes, contribuindo para uma gestão agrícola mais eficiente, sustentável e orientada por dados.*


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: Pasta destinada ao armazenamento de imagens, diagramas, capturas de tela e demais recursos visuais utilizados na documentação e apresentação do projeto.

- <b>data</b>: Contém os arquivos de dados utilizados pela solução.
   - <code>simulated_sensor_readings.csv</code>: dataset simulado utilizado para popular o banco de dados com registros históricos para treinamento e validação dos modelos de Machine Learning.

- <b>dashboard</b>: Contém a aplicação analítica desenvolvida para visualização dos dados e resultados do projeto.
   - <code>app.py</code>: dashboard interativo responsável pela exibição de métricas, correlações, previsões agrícolas e tendências de produtividade.

- <b>database</b>: Contém os módulos responsáveis pela conexão e manipulação do banco de dados Oracle.
   - <code>database.py</code>: realiza a conexão com o banco de dados e inicialização da estrutura necessária para a aplicação.
   - <code>sensor_reading_repository.py</code>: centraliza as operações de consulta e persistência das leituras agrícolas armazenadas.
 
- <b>ml</b>: Contém os componentes relacionados ao treinamento, avaliação e execução dos modelos de Machine Learning.
   - <code>dataset_builder.py</code>: realiza a extração e preparação dos dados armazenados no banco para utilização nos modelos preditivos.
   - <code>train_models.py</code>: responsável pelo treinamento dos modelos de regressão, cálculo das métricas de desempenho e geração dos artefatos necessários para previsões futuras.
   - <code>prediction_service.py</code>: executa previsões agrícolas utilizando os modelos previamente treinados e gera recomendações de irrigação e manejo agrícola.
   - <code>trained_models</code>: diretório utilizado para armazenamento local dos modelos treinados gerados durante a execução da aplicação.
 
- <b>services</b>: Contém os serviços auxiliares utilizados pela aplicação.
   - <code>automatic_ingestion_service.py</code>: realiza a ingestão automática e periódica das leituras dos sensores para o banco de dados.
   - <code>csv_import_service.py</code>: realiza a importação de datasets simulados para popular a base histórica utilizada pelos modelos preditivos.
   - <code>dashboard_launcher.py</code>: responsável por iniciar automaticamente o dashboard Streamlit a partir do menu principal da aplicação.

- <b>include</b>: Contém os arquivos de cabeçalho da aplicação embarcada, responsáveis pelas definições de estruturas, funções e contratos utilizados pelo projeto.
   - <code>pins.h</code>: define o mapeamento dos pinos utilizados pelos sensores conectados ao ESP32.
   - <code>sensor_readings.h</code>: define as estruturas e funções responsáveis pela leitura dos sensores agrícolas.
   - <code>productivity_engine.h</code>: define as funções responsáveis pelo cálculo do índice de produtividade esperada.
   - <code>recommendation_engine.h</code>: define as regras utilizadas para geração das recomendações agrícolas.
   - <code>serial_logger.h</code>: define as funções responsáveis pela exibição estruturada das informações no monitor serial.

- <b>src</b>: Contém o código fonte da solução, incluindo a aplicação embarcada no ESP32 e a aplicação Python.
   - <code>main.ino</code>: ponto de entrada da aplicação embarcada no ESP32, responsável pela leitura dos sensores agrícolas simulados.
   - <code>sensor_readings.cpp</code>: realiza a leitura, conversão e formatação dos dados provenientes dos sensores.
   - <code>productivity_engine.cpp</code>: calcula o índice de produtividade esperada com base nos indicadores agrícolas coletados.
   - <code>recommendation_engine.cpp</code>: executa as regras de negócio responsáveis pelas recomendações locais de irrigação e manejo agrícola.
   - <code>serial_logger.cpp</code>: responsável pela exibição estruturada das leituras no monitor serial.
   - <code>main.py</code>: ponto de entrada da aplicação Python responsável pela inicialização do banco de dados e carregamento do menu principal.
   - <code>menu.py</code>: implementa o menu interativo utilizado para consulta dos sensores, persistência dos dados, treinamento dos modelos, execução das previsões e abertura do dashboard.

- <b>.env</b>: arquivo local utilizado para armazenamento das credenciais de acesso ao banco de dados Oracle.

- <b>.env.example</b>: modelo de configuração das variáveis de ambiente necessárias para utilização das integrações externas.

- <b>requirements.txt</b>: lista as dependências Python necessárias para execução completa da aplicação.

- <b>platformio.ini</b>: arquivo de configuração do PlatformIO, responsável por definir o ambiente de build, dependências e execução da aplicação embarcada.

- <b>diagram.json</b>: Define a configuração do circuito no Wokwi, incluindo ESP32, sensores e conexões.

- <b>wokwi.toml</b>: arquivo de configuração da integração entre PlatformIO e simulador Wokwi.

- <b>README.md</b>: Arquivo que apresenta uma visão geral do projeto, incluindo sua finalidade, estrutura e instruções de uso.


## 🔌 Representação do circuito

<p align="center">
  <img src="assets/wokwiCircuit.png" width="600"/>
</p>

<p align="center">
  <i>Figura 1 — Diagrama do circuito simulado no Wokwi</i>
</p>


## 📎 Links e Observações

- <b>Listagem de Links</b>: Links do projeto (ex. vídeos da entrega, páginas, etc.),
   - Vídeo demonstrativo: [Assistir no YouTube](https://youtu.be/lNG4tYj-Chc)

- <b>Explicação de decisões técnicas</b>:
   - Para simplificar a simulação dos dados agrícolas no ambiente Wokwi, foram utilizados potenciômetros para representar algumas variáveis do campo, como umidade do solo, pH e nível de nutrientes. Essa abordagem permitiu gerar valores controlados e compatíveis com as regras do projeto, mantendo o foco principal da atividade na integração dos dados, construção dos modelos preditivos e desenvolvimento do dashboard analítico.
   - O índice de produtividade esperada foi desenvolvido como um indicador agronômico composto, calculado a partir da combinação de fatores considerados relevantes para o desenvolvimento da lavoura, como umidade do solo, pH, luminosidade e nível de nutrientes. Esse índice foi utilizado tanto para análises quanto para treinamento dos modelos preditivos.
   - Para aumentar a quantidade de registros disponíveis para treinamento dos modelos de Machine Learning, foi adotada a importação opcional de um dataset simulado contendo dados agrícolas historicamente consistentes. Essa estratégia permitiu trabalhar com uma base mais robusta, melhorando a qualidade das previsões geradas pelos modelos.
   - O banco de dados é utilizado como repositório central da solução. Todas as leituras dos sensores são armazenadas juntamente com os indicadores calculados pelo sistema, como produtividade esperada e volume de irrigação recomendado, formando o histórico utilizado pelos modelos preditivos.
   - As previsões agrícolas são realizadas utilizando a leitura mais recente registrada no banco de dados como cenário atual. Dessa forma, o fluxo adotado pela solução consiste em: coleta dos sensores, cálculo dos indicadores agrícolas, persistência dos dados no banco e execução das previsões a partir do histórico armazenado. Quando a ingestão automática está ativa, as previsões passam a refletir continuamente os dados mais recentes coletados pelo sistema.
   - Como o projeto possui caráter acadêmico e não utiliza séries temporais reais de longo prazo, as previsões não representam estimativas para uma data específica futura. Os resultados devem ser interpretados como um cenário agrícola estimado pelo modelo com base nos padrões identificados no histórico de dados utilizado durante o treinamento.
   - O volume de irrigação previsto foi modelado como um problema de regressão, permitindo que o sistema estime quantitativamente a necessidade de irrigação a partir das condições agrícolas observadas. Essa abordagem possibilita gerar recomendações mais precisas do que uma simples decisão binária de irrigar ou não irrigar.
   - A necessidade de fertilização foi representada por meio de classificações qualitativas (Baixa, Média e Alta), facilitando a interpretação dos resultados pelos usuários e permitindo a geração de recomendações de manejo agrícola mais intuitivas.
   - Os modelos de Machine Learning foram desenvolvidos utilizando aprendizado supervisionado de regressão para prever variáveis críticas do campo, incluindo umidade do solo, pH, nível de nutrientes, produtividade esperada e volume de irrigação. O desempenho dos modelos é avaliado por meio das métricas MAE, MSE, RMSE e R², permitindo analisar a qualidade das previsões geradas.
   - O dashboard analítico foi desenvolvido para consolidar os dados históricos, métricas dos modelos, correlações entre variáveis agrícolas, tendências de produtividade e previsões geradas pelo sistema, oferecendo uma visão integrada das informações utilizadas na tomada de decisão agrícola.


## 🔧 Como executar o código

*Pré Requisitos:*

*Git - Utilizado para clonar o repositório do projeto.*

*Visual Studio Code (VS Code)*

*Extensões: PlatformIO, Wokwi Simulator, pyserial e python-dotenv* 

*Se necessário instalar os certificados SSL do Python*

*Garantir que tenha as instalações necessárias das linguagens C/C++ e Python*

*Criar credenciais OAuth2 no Sentinel Hub*

*Criar um projeto no Supabase e configurar as tabelas <code>atmosphere_raw_payloads</code> e <code>atmosphere_records</code>*

*Configurar as variáveis de ambiente do Supabase no arquivo .env*

*Instalar as dependências Python com `pip install -r requirements.txt`*

*Fase 1 — Clonar o repositório:*

*No terminal, execute: git clone `git@github.com:renatoruiz2607/fiapGroupRepository.git`*

*Em seguida, faça o trajeto até a pasta principal:*

*cd fiapGroupRepository*

*cd 1TIAO*

*cd Global-Solution-1*

*Crie e configure o arquivo .env com as informações de .env.example*

*Fase 2 — Executar a aplicação*

*Abra a extensão PlatformIO*

*Execute o build*

*Abra a extensão Wokwi Simulator*

*Clique em Start Simulation*

*No terminal python, execute `python3 src/main.py`*

*Fase 3 - Funcionamento*

*O sistema permite, pelo menu interativo:*

- *cadastrar um nome e receber um UUID*
- *cadastrar uma região com latitude e longitude*
- *Conferir os valores detectados nos sensores*

*O sistema também permite simular diferentes cenários em tempo real via alteração dos níveis dos sensores, a partir dos componentes no simulador Wokwi (diagram.json)*

- *Conferir valores importantes para a análise da qualidade do ar nas APIs Nasa Power e Sentinel-5P*
- *Receber a análise lógica do sistema para aquela região*
- *Enviar os dados daquela região e de outras que vão se acumulando no histórico ao banco de dados Supabase*
- *Abertura do Dashboard no navegador*

*O usuário informa seu UUID no dashboard para consultar diretamente os dados armazenados no Supabase, visualizando métricas, gráficos, rankings e informações analíticas sobre as regiões monitoradas.*

*O usuário pode também inserir um CSV no dashboard para realizar consultas.*

## 🧠 Lógica de Análise Atmosférica

*A análise baseada em regras é responsável por interpretar os dados coletados pelos sensores locais, NASA POWER e Sentinel-5P, gerando o score de recuperação atmosférica, o status da região, a comparação entre cenário local e regional e uma recomendação final.*

### Cálculo do Ozone Recovery Score

*O ozone_recovery_score é calculado com base em dois fatores principais:*

- *impacto da poluição atmosférica;*
- *bônus de recuperação ambiental.*

*A lógica considera que altas concentrações de poluentes reduzem o score, enquanto condições favoráveis de dispersão e limpeza atmosférica aumentam o score.*

*Fórmula aplicada:*

*score = 75 - (pollution_score * 55) + (recovery_bonus * 20)*

*O resultado final é limitado entre 0 e 100.*

### Pollution Score

*O pollution_score considera os principais indicadores de degradação atmosférica:*

- *NO₂;*
- *CO;*
- *SO₂;*
- *qualidade do ar local.*

*Cada variável é normalizada para uma escala de 0 a 1 e recebe um peso na composição do impacto ambiental.*

*pollution_score = (NO₂ * 0.30) + (CO * 0.25) + (SO₂ * 0.25) + (local_air_quality * 0.20)*

*Quanto maior o pollution_score, maior o impacto negativo sobre o potencial de recuperação atmosférica.*

### Recovery Bonus

*O recovery_bonus considera variáveis que favorecem a dispersão ou redução de poluentes:*

- *velocidade do vento;*
- *precipitação;*
- *umidade relativa do ar.*

*recovery_bonus = (wind_speed * 0.40) + (rainfall * 0.35) + (humidity * 0.25)*

*Quanto maior o recovery_bonus, melhores são as condições ambientais para dispersão ou remoção de poluentes.*

### Status de Recuperação

*Após o cálculo do score, a região é classificada em uma das seguintes categorias:*

- *score >= 80  → Em Recuperação*
- *score >= 50  → Estável*
- *score < 50   → Em Degradação*

### Comparação Local x Regional

*A comparação entre dados locais e regionais é utilizada para identificar se o problema atmosférico está concentrado próximo aos sensores ou se possui comportamento mais amplo na região.*

*A qualidade regional é analisada com base em NO₂, CO e SO₂.*

*Regional ruim: NO₂ > 0.00006 ou CO > 0.05 ou SO₂ > 0.000012*

*A qualidade local é analisada com base no valor de local_air_quality obtido pelo sensor MQ2.*

- *local_air_quality >= 3000 → ruim*
- *local_air_quality >= 1800 → atenção*
- *local_air_quality < 1800  → bom*

*Com base nesses cenários, o sistema classifica a comparação da seguinte forma:*

*Regional bom + Local ruim/atenção*
→ *Anomalia Local Detectada*

*Regional ruim + Local bom*
→ *Influência Atmosférica Regional*

*Regional ruim + Local ruim/atenção*
→ *Degradação Atmosférica Generalizada*

*Regional bom + Local bom*
→ *Condições Atmosféricas Favoráveis*

### Recomendação Automática

*A recomendação é gerada de acordo com o resultado da comparação local x regional e com os poluentes mais críticos identificados.*

*Quando há anomalia local, o sistema recomenda investigar fontes próximas de emissão, como tráfego intenso, indústrias, queimadas ou fontes pontuais de poluição.*

*Quando há influência atmosférica regional, o sistema indica que poluentes podem ter sido transportados de regiões distantes, possivelmente pela ação dos ventos.*

*Quando há degradação generalizada, o sistema recomenda intensificar ações de controle de emissões e ampliar o monitoramento local e regional.*

*Quando as condições são favoráveis, o sistema recomenda manter o monitoramento contínuo da região.*

*Caso nenhum cenário específico seja identificado, o sistema avalia os poluentes individualmente:*

- *NO₂ elevado → reduzir emissões veiculares e monitorar corredores de tráfego urbano*
- *SO₂ elevado → investigar possíveis fontes industriais*
- *CO elevado → monitorar combustão, queimadas e emissões por veículos*

*Essa lógica garante que a análise seja explicável, rastreável e alinhada ao objetivo do projeto, permitindo demonstrar como os dados locais e regionais são combinados para apoiar decisões ambientais e consequentemente auxiliar na regeneração da camada de ozônio.*

## 🗄️ Integração com Supabase e Dashboard

*A integração com Supabase foi implementada para permitir que os registros ambientais gerados pela aplicação sejam persistidos em banco de dados e posteriormente consumidos pelo dashboard analítico.*

*O envio dos dados ocorre a partir do histórico local gerado pela aplicação. Cada análise concluída contém informações da região monitorada, dados climáticos da NASA POWER, dados atmosféricos do Sentinel-5P, leituras dos sensores locais e resultado da análise baseada em regras.*

*Para garantir rastreabilidade e flexibilidade, os dados são armazenados em duas tabelas:*

- *<code>atmosphere_raw_payloads</code>: armazena o JSON completo da análise em formato JSONB, preservando todos os campos originais gerados pela aplicação.*
- *<code>atmosphere_records</code>: armazena os principais campos da análise em colunas estruturadas, facilitando consultas, filtros, gráficos e análises no dashboard.*

*Cada usuário possui um identificador único em formato UUID. Esse identificador é gerado pela aplicação e associado aos registros enviados ao Supabase, permitindo que o dashboard filtre os dados correspondentes ao usuário informado.*

*O dashboard foi desenvolvido em Streamlit e conectado diretamente ao Supabase. A visualização apresenta indicadores como total de registros, score médio, menor score, quantidade de registros em degradação, evolução do score atmosférico, distribuição por status, ranking de regiões e comparação média de poluentes.*

*As variáveis necessárias para conexão com o Supabase são configuradas no arquivo <code>.env</code>:*

```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
SUPABASE_RAW_TABLE=atmosphere_raw_payloads
SUPABASE_RECORDS_TABLE=atmosphere_records


Para executar o dashboard localmente, utilize a função 10 do menu.
```

## 📊 Dashboard Analítico

*O dashboard analítico foi desenvolvido em Streamlit e conectado diretamente ao Supabase, permitindo que os dados persistidos no banco sejam consultados por meio do UUID do usuário.*

*Além disso, há também a opção de importar um arquivo CSV para análise dos registros, possibilitando a utilização do dashboard mesmo sem conexão com o banco de dados.*

*A interface apresenta métricas gerais, filtros, gráficos e uma tabela com os registros ambientais coletados e analisados pelo sistema.*

*Para complementar as análises, foi implementada uma camada de Machine Learning utilizando os algoritmos Random Forest Regressor e Random Forest Classifier, ambos disponibilizados pela biblioteca Scikit-Learn. O Random Forest Regressor é utilizado para prever o Ozone Recovery Score de cada região, enquanto o Random Forest Classifier é utilizado para prever o status de recuperação atmosférica e a recomendação mais provável para a região analisada.*

*As predições são apresentadas por região, permitindo visualizar o score médio atual, o score previsto pelo modelo e a tendência estimada (melhora, estabilidade ou piora), além do status e recomendação previstos para a região selecionada.*

*Para avaliar a qualidade das previsões, é utilizado o indicador MAE (Mean Absolute Error ou Erro Médio Absoluto), uma métrica que mede a diferença média entre os valores reais e os valores previstos pelo modelo. Quanto menor o valor do MAE, maior a precisão das previsões realizadas pelo algoritmo.*

*Link do dashboard publicado no Render:*

- <a href="https://dashboardgloabalsolutionfiap.onrender.com" target="_blank">Acessar Dashboard Ozone Recovery Intelligence</a>

### Tela Inicial do Dashboard

<p align="center">
  <img src="assets/dashboard/launchPage.png" width="800"/>
</p>
<p align="center"><i>Figura 2 — Tela inicial do dashboard com campo para informar o UUID do usuário</i></p>

### Métricas e Análises Visuais

<p align="center">
  <img src="assets/dashboard/dataPage1.png" width="800"/>
</p>

<p align="center">
  <i>Figura 3 — Cards de métricas e gráficos de evolução do score e distribuição por status</i>
</p>

### Ranking, Poluentes e Registros

<p align="center">
  <img src="assets/dashboard/dataPage2.png" width="800"/>
</p>

<p align="center">
  <i>Figura 4 — Cards de métricas e gráficos de evolução do score e distribuição por status</i>
</p>

### Predições com Machine Learning

<p align="center">
  <img src="assets/dashboard/dataPage3.png" width="800"/>
</p>

<p align="center">
  <i>Figura 5 — Seção com predições por região com Machine Learning</i>
</p>


## 🗃 Histórico de lançamentos

* 1.0.0 - 16/06/2026
    *
* 0.8.0 - 15/06/2026
    * 
* 0.7.0 - 15/06/2026
    * 
* 0.6.0 - 15/06/2026
    * 
* 0.5.0 - 15/06/2026
    * 
* 0.4.0 - 14/06/2026
    * 
* 0.3.0 - 14/06/2026
    * 
* 0.2.0 - 14/06/2026
    * 
* 0.1.0 - 14/06/2026
    *

---


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
