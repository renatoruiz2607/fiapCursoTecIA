# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://raw.githubusercontent.com/agodoi/template/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Farm Tech Analytics

## Grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/renatoruizcai">Renato Ruiz Cai</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>


## 📜 Descrição

*O Farm Tech Analytics é o projeto desenvolvido para simular o cenário da FarmTech Solutions para o agronegócio que presta consultoria a uma fazenda de médio porte responsável pelo cultivo de diferentes culturas agrícolas.*

*A partir da base de dados `crop_yield.csv`, contendo variáveis climáticas (precipitação, umidade específica, umidade relativa e temperatura) e o rendimento de safra observado para quatro culturas distintas, o projeto aplica a metodologia CRISP-DM para responder a dois objetivos centrais: prever o rendimento de safra por meio de Regressão Supervisionada e explorar a tendência de produtividade da fazenda por meio de Machine Learning Não Supervisionado.*

*O notebook percorre todo o fluxo analítico: análise exploratória dos dados, identificação de outliers, análise de correlação e estatísticas descritivas, seguida de uma etapa de clusterização com K-Means para investigar padrões climáticos e possíveis cenários discrepantes. Na sequência, cinco algoritmos de regressão são treinados, comparados e otimizados para estimar o rendimento de safra a partir da cultura plantada e das condições climáticas, com avaliação por meio de métricas como MAE, RMSE e R².*

*Complementarmente, o projeto apresenta uma estimativa de custos de infraestrutura na AWS, utilizando a AWS Pricing Calculator para comparar o custo de hospedar, sob demanda, uma máquina Linux simples destinada a receber os dados dos sensores e executar o modelo de Machine Learning, contrastando as regiões de São Paulo e Norte da Virgínia e discutindo o equilíbrio entre custo, restrições legais de armazenamento de dados e latência de acesso.*

*O objetivo do projeto é demonstrar, de ponta a ponta, como dados agrícolas podem ser explorados, modelados e operacionalizados em nuvem para apoiar decisões mais inteligentes de manejo agrícola.*


## 📁 Estrutura

Dentre os arquivos presentes na raiz do projeto, definem-se:

- <b>RenatoRuizCai_RM572235_fase5_cap1.ipynb</b>: notebook desenvolvido no Google Colab para o projeto FarmTech Solutions. Aplica a metodologia CRISP-DM sobre a base `crop_yield.csv` para realizar uma análise exploratória completa (tipos de dados, valores nulos, identificação de outliers, correlação e estatísticas descritivas), explorar a tendência de produtividade por meio de clusterização com K-Means, com escolha do número de clusters via Elbow e Silhouette Score (Machine Learning Não Supervisionado), e treinar, comparar e otimizar cinco modelos de Regressão Supervisionada (Regressão Linear, KNN, SVR, Árvore de Decisão e Random Forest) para prever o rendimento de safra a partir da cultura plantada e das variáveis climáticas, avaliados por MAE, RMSE e R².

- <b>crop_yield.csv</b>: Dataset utilizado nas análises.

- <b>README.md</b>: Arquivo que apresenta uma visão geral do projeto, incluindo sua finalidade, estrutura e instruções de uso.


## 📎 Links e Observações

- <b>Listagem de Links</b>: Links do projeto (ex. vídeos da entrega, páginas, etc.),
   - Vídeo demonstrativo do Colab: [Assistir no YouTube](https://youtu.be/G1jIB4fp30I)
   - Vídeo demonstrativo do AWS Princig: [Assistir no YouTube](https://youtu.be/pohpE9_sJuc)

- <b>Explicação de decisões técnicas</b>:
   - No `RenatoRuizCai_RM572235_fase5_cap1.ipynb`, o pré-processamento das variáveis climáticas (padronização) e da variável categórica cultura (One-Hot Encoding) foi encapsulado em Pipelines com ColumnTransformer, evitando vazamento de dados (data leakage) entre os conjuntos de treino e teste durante o treinamento e a otimização dos modelos.
   - A divisão entre treino e teste (70%/30%) foi estratificada pela variável cultura, garantindo que as quatro culturas presentes na base mantivessem a mesma proporção nos dois conjuntos.
   - A identificação de outliers foi feita em duas camadas complementares: método do Intervalo Interquartil (IQR) na análise exploratória — aplicado tanto na base completa quanto separadamente por cultura, para evitar falsos positivos causados pela mistura de escalas de rendimento entre culturas muito diferentes — e distância ao centróide na etapa de clusterização.
   - O número de clusters (k=4) utilizado na análise de tendência de produtividade foi definido combinando o método do Cotovelo (Elbow) e o Silhouette Score, e não apenas um critério isolado, buscando equilíbrio entre qualidade do agrupamento e interpretabilidade dos resultados.
   - Foi realizado um experimento de controle, treinando um modelo apenas com as variáveis climáticas (sem a variável cultura), para validar quantitativamente o peso real de cada grupo de variáveis na previsão do rendimento de safra.
   - Os cinco modelos de Regressão Supervisionada (Regressão Linear, KNN, SVR, Árvore de Decisão e Random Forest) foram otimizados com GridSearchCV (validação cruzada de 5 folds, métrica R²), e a escolha do modelo final considerou não apenas a métrica no conjunto de teste, mas também o risco de overfitting — preferindo o Random Forest otimizado a uma Árvore de Decisão sem restrição de profundidade.


## 🔧 Como executar o código

***Pré Requisitos:***

*Baixar o arquivo `crop_yield.csv.`*

***Funcionamento:***

*Abrir o arquivo `RenatoRuizCai_RM572235_fase5_cap1.ipynb`*

*Clicar no botão `Open in Colab`*

*No menu lateral esquerdo, selecione `Arquivos`*

*Na tab Arquivos, selecione `Fazer upload para o armazenamento da sessão`*

*Importe o arquivo `crop_yield.csv.`*

*Após isso, no conteúdo principal, cada bloco de código contém um botão executar*

*Vá executando todos de cima abaixo, não pule nenhum, para que tudo rode corretamente.*


## 💵 Estimativa de Custos AWS (AWS Pricing Calculator)

*Foi realizada uma estimativa de custos On-Demand (100% de utilização) na AWS Pricing Calculator para uma máquina Linux simples, destinada a hospedar a API que receberia os dados dos sensores e executaria o modelo de Machine Learning.*

*A configuração utilizada foi uma instância Amazon EC2 t4g.micro (2 vCPUs, 1 GiB de memória, rede de até 5 Gigabit, arquitetura Graviton2/ARM), com volume Amazon EBS gp3 de 50 GB, contratação sob demanda (On-Demand) e locação compartilhada, comparando as regiões São Paulo (sa-east-1) e Norte da Virgínia (us-east-1).*

*Considerando apenas o custo da instância e do armazenamento, a região de Norte da Virgínia apresenta o menor valor mensal estimado — cerca de USD 10,13/mês (USD 0,0084/hora pela instância + USD 0,08/GB-mês pelo armazenamento gp3) — contra aproximadamente USD 17,38/mês em São Paulo (USD 0,0134/hora pela instância + USD 0,152/GB-mês pelo armazenamento gp3), cerca de 71% mais cara.*

*Apesar disso, para o cenário da FarmTech Solutions optamos pela região de São Paulo, mesmo sendo a opção mais cara, pelos seguintes motivos:*

- *<b>Restrição legal de armazenamento</b>: partindo da premissa de que há restrições legais para armazenar os dados no exterior, a região de Norte da Virgínia fica automaticamente descartada, independentemente do custo, pois armazenaria os dados dos sensores fora do território nacional.*
- *<b>Latência e velocidade de acesso</b>: os sensores estão fisicamente instalados na fazenda, no Brasil. Hospedar a API e os dados em São Paulo reduz significativamente o tempo de resposta (poucos milissegundos dentro do Brasil, contra 120–160ms ou mais até a Norte da Virgínia), o que é essencial para o acesso rápido aos dados dos sensores exigido pela atividade.*

*Ou seja, a alternativa financeiramente mais barata nem sempre é a tecnicamente adequada: quando existem exigências legais de residência dos dados e necessidade de baixa latência, a escolha da região deixa de ser puramente uma decisão de custo e passa a ser uma decisão de viabilidade.* 

*Outro ponto importante é que as instâncias t3.micro, t3a.micro e t4g.micro apresentam configurações semelhantes em termos de capacidade, oferecendo 2 vCPUs, 1 GiB de memória e desempenho de rede de até 5 Gbps. A principal diferença está na arquitetura dos processadores: as famílias T3 e T3a utilizam arquitetura x86_64, com processadores Intel e AMD, respectivamente, enquanto a T4g utiliza processadores AWS Graviton baseados em arquitetura ARM64.*

*Para o cenário proposto, a t4g.micro é uma alternativa adequada por atender aos requisitos de processamento, memória e rede definidos, apresentando ainda menor custo por hora sob demanda entre as opções avaliadas.*

*Atualmente, o projeto consiste em uma solução analítica de Machine Learning desenvolvida em Python no Google Colab, responsável por processar e analisar dados provenientes de um arquivo CSV. Portanto, não existem dependências que justifiquem a necessidade específica de uma arquitetura x86.*

*Mesmo considerando uma evolução para um cenário real, com sensores físicos enviando dados para uma aplicação desenvolvida em Python e utilizando MySQL para persistência, a arquitetura ARM64 da T4g continuaria sendo compatível com esse tipo de solução, desde que as bibliotecas e demais dependências utilizadas possuam suporte a ARM64. Dessa forma, para a arquitetura proposta, a t4g.micro oferece capacidade compatível com a necessidade do projeto e melhor custo-benefício.*


---


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
