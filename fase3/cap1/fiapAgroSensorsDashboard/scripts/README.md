# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://raw.githubusercontent.com/agodoi/template/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Sensors Database


## 📜 Descrição

*O projeto utiliza o Oracle Database com o SQL Developer para armazenar e consultar os dados simulados de sensores agrícolas presentes no dataset `irrigation_training_data.csv`.*

*A base foi estruturada para representar um cenário de monitoramento inteligente de irrigação, contendo dados como umidade do solo, pH, nutrientes, potássio, previsão de chuva e recomendação de irrigação.*

*Por meio das consultas SQL, foi possível analisar padrões dos sensores, identificar cenários críticos e preparar os dados para futuras análises preditivas e modelos de inteligência artificial.*


## 📋 Passos seguidos

*Seguido o passo a passo da introdução da atividade no portal FIAP e importado o dataset `irrigation_training_data.csv`*


## 🔎 Primeiras descobertas

*Ao verificar o dataset importado foi observado que a coluna PH_VALUE era do tipo VARCHAR, o que poderia atrapalhar em algumas consultas, como por exemplo a de média.*

*Para resolver isso foi realizada a criação de uma nova coluna numérica chamada `PH_VALUE_NUM`*

*Logo após foi feita a conversão dos dados da coluna `PH_VALUE` para numéricos com a função `TO_NUMBER` e atribuídos os valores convertidos para a nova coluna `PH_VALUE_NUM`*

*E para finalizar a coluna original foi removida com `DROP COLUMN` e a nova coluna renomeada com `RENAME COLUMN` para mantermos o nome original dela.*


## 📊 Análise dos Dados

**1. Consulta da base completa de dados**

<p align="center">
  <img src="assets/selectFromSensores.png" width="600"/>
</p>

<p align="center">
  <i>Base completa de dados</i>
</p>

**2. Consulta da quantidade total de registros**

<p align="center">
  <img src="assets/countTotalRegistros.png" width="600"/>
</p>

<p align="center">
  <i>Quantidade total de registros</i>
</p>

**3. Consulta da distribuição e percentual da decisão de irrigação**

*A consulta permitiu identificar a distribuição das decisões de irrigação presentes no dataset. Os resultados demonstram que **60%** dos registros indicam cenários em que a irrigação não é recomendada, enquanto **40%** representam situações em que o sistema recomenda irrigar.*

<p align="center">
  <img src="assets/distPctDecisaoIrrigacao.png" width="600"/>
</p>

<p align="center">
  <i>Distribuição e percentual da decisão de irrigação</i>
</p>

**4. Consulta das médias dos sensores por decisão de irrigação**

*A consulta permitiu analisar o comportamento médio dos sensores em cenários onde o sistema recomenda ou não a irrigação. Os resultados demonstram que os casos com recomendação de irrigação apresentam menor média de umidade do solo, indicando que esse é um dos principais fatores considerados na decisão.*

*Também foi possível observar pequenas variações nos níveis médios de pH, nutrientes ativos e presença de potássio entre os cenários analisados. Além disso, os registros sem recomendação de irrigação apresentaram maior média de previsão de chuva, reforçando a influência das condições climáticas no processo de decisão.*

<p align="center">
  <img src="assets/meanByDecisao.png" width="600"/>
</p>

<p align="center">
  <i>Médias dos sensores por decisão de irrigação</i>
</p>

**5. Consulta dos cenários críticos com baixa umidade e recomendação de irrigação**

*A consulta permitiu identificar cenários críticos em que a umidade do solo estava abaixo de **40%**, levando o sistema a recomendar a irrigação. Foram encontrados **26** registros com esse comportamento, indicando situações de possível estresse hídrico para a plantação.*

*Os resultados demonstram que baixos níveis de umidade possuem forte influência na tomada de decisão do sistema, principalmente quando combinados com ausência de previsão de chuva e condições adequadas de nutrientes e potássio no solo.*

<p align="center">
  <img src="assets/criticalLowMoisture.png" width="600"/>
</p>

<p align="center">
  <i>Cenários críticos com baixa umidade e recomendação de irrigação</i>
</p>

**6. Consulta dos casos em que há baixa umidade, mas o sistema não recomenda irrigar**

*Os resultados demonstram que variáveis como nível de pH, quantidade de nutrientes ativos, presença de potássio e previsão de chuva também influenciam diretamente na recomendação final do sistema de irrigação.*

*Mesmo em cenários com baixa umidade do solo, a irrigação não foi recomendada quando havia algum fator de restrição, como pH fora da faixa adequada, previsão de chuva, baixa quantidade de nutrientes ativos ou ausência de potássio. Isso demonstra que o sistema considera múltiplas variáveis antes de recomendar a irrigação, evitando decisões baseadas apenas na umidade do solo.*

*No dataset, os principais motivos parecem ser:*
- *pH fora da faixa ideal: **9** registros*
- *Previsão de chuva: **6** registros*
- *Nutrientes insuficientes: **6** registros*
- *Potássio ausente: **3** registros*

<p align="center">
  <img src="assets/lowMoistureIrrigationOff.png" width="600"/>
</p>

<p align="center">
  <i>Cenários com baixa umidade e recomendação de não irrigar</i>
</p>

**7. Consulta do impacto da previsão de chuva na decisão**

*A consulta demonstrou que a previsão de chuva possui forte influência na decisão do sistema de irrigação. Todos os registros com previsão de chuva indicaram cenários em que a irrigação não foi recomendada, mesmo quando outras condições poderiam favorecer a irrigação.*

<p align="center">
  <img src="assets/rainImpact.png" width="600"/>
</p>

<p align="center">
  <i>Impacto da previsão de chuva na decisão</i>
</p>

**8. Consulta do impacto do potássio na decisão de irrigação**

*A consulta demonstrou que a presença de potássio possui influência direta na recomendação de irrigação. Todos os cenários em que o potássio estava ausente resultaram em decisões sem irrigação, indicando que o sistema considera esse nutriente como um fator essencial para a saúde e equilíbrio do solo.*

<p align="center">
  <img src="assets/potassiumImpact.png" width="600"/>
</p>

<p align="center">
  <i>Impacto do potássio na decisão de irrigação</i>
</p>

**9. Consulta dos registros por faixa de umidade do solo**

*A consulta permitiu classificar os registros em faixas de umidade do solo, possibilitando analisar como cada nível influencia a decisão de irrigação. Os resultados demonstram que cenários de umidade baixa apresentaram maior concentração de recomendações para irrigar, enquanto os cenários de umidade alta resultaram exclusivamente em decisões sem irrigação.*

*Também foi possível observar que os casos de umidade moderada ficaram mais distribuídos entre irrigar e não irrigar, indicando que nessa faixa outros fatores, como previsão de chuva, nutrientes e condições químicas do solo, possuem maior influência na decisão final do sistema.*

<p align="center">
  <img src="assets/moistureCategories.png" width="600"/>
</p>

<p align="center">
  <i>Registros por faixa de umidade do solo</i>
</p>

**10. Consulta dos registros ideais para treinamento do modelo com recomendação de irrigação**

*Consulta realizada para identificar registros ideais para treinamento do modelo, onde todos os critétios para irrigação estão sendo atendidos.*

<p align="center">
  <img src="assets/idealTrainingScenarios.png" width="600"/>
</p>

<p align="center">
  <i>Rregistros ideais para treinamento do modelo</i>
</p>

## 🎥 Vídeo demonstrativo

▶️ [Assistir no YouTube](https://youtu.be/z8qphi9TDIA)


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


