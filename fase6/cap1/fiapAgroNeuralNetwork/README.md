# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://raw.githubusercontent.com/agodoi/template/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Agro Neural Network

## Grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/renatoruizcai">Renato Ruiz Cai</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>


## 📜 Descrição

*Este projeto apresenta uma aplicação prática de Visão Computacional, explorando diferentes abordagens de Inteligência Artificial para reconhecer dois objetos do cotidiano: um controle de PlayStation 5 (PS5) e uma garrafa térmica.*

*A proposta é investigar como diferentes modelos de aprendizado profundo (Deep Learning) interpretam imagens e identificam objetos, considerando suas características, capacidades e limitações.*

*Para isso, foram utilizadas três abordagens:*

*YOLOv5 adaptável: modelo pré-treinado e posteriormente ajustado com imagens dos objetos selecionados, utilizando treinamentos de 30 e 60 épocas para detectar e localizar os objetos nas imagens.*

*YOLOv5 padrão: modelo utilizado com seus pesos originais, sem treinamento adicional, permitindo observar como uma rede treinada em categorias genéricas reconhece os objetos do projeto.*

*CNN construída do zero: rede neural convolucional desenvolvida especificamente para classificar as imagens entre controle PS5 e garrafa térmica, sem utilizar pesos pré-treinados.*

*O projeto utiliza um conjunto de 94 imagens, distribuídas entre treinamento, validação e teste, permitindo avaliar o comportamento dos modelos em diferentes condições.*

*Além da implementação, o repositório apresenta exemplos visuais das detecções e classificações realizadas, incluindo imagens reconhecidas corretamente, identificações incorretas e situações em que os modelos não conseguiram reconhecer os objetos.*

*O objetivo é demonstrar, de maneira prática, as diferenças entre detecção e classificação de imagens, destacando como o treinamento personalizado influencia o reconhecimento de objetos e como cada abordagem responde aos mesmos dados.*

*A documentação técnica, os procedimentos de treinamento, as métricas e as análises quantitativas estão disponíveis no notebook do Google Colab. Este README concentra-se na apresentação do funcionamento do projeto, na organização dos experimentos e na análise visual dos resultados, complementando o conteúdo técnico do notebook.*


## 📁 Estrutura

Dentre os arquivos presentes na raiz do projeto, definem-se:

- <b>RenatoRuiz_rm572235_pbl_fase6.ipynb</b>: notebook desenvolvido no Google Colab para um projeto de Visão Computacional, utilizando técnicas de Deep Learning para detecção e classificação de controles PS5 e garrafas térmicas. Contempla a preparação e validação de um dataset com 94 imagens, o treinamento e a avaliação de dois modelos YOLOv5s adaptáveis (30 e 60 épocas), a execução do YOLOv5s padrão com pesos pré-treinados no COCO e a construção de uma Rede Neural Convolucional (CNN) do zero com TensorFlow/Keras. Inclui o processamento e a visualização das imagens, a avaliação dos modelos por meio de métricas como Precision, Recall, F1-score, acurácia, mAP e matriz de confusão, além da medição dos tempos de treinamento e inferência. Apresenta análises técnicas e comparativas dos resultados, destacando as diferenças de desempenho, as limitações e as características de cada abordagem..

- <b>README.md</b>: Arquivo que apresenta uma visão geral do projeto, incluindo sua finalidade, estrutura e instruções de uso.


## 📎 Links e Observações

- <b>Listagem de Links</b>: Links do projeto (ex. vídeos da entrega, páginas, etc.),
   - Vídeo demonstrativo do Colab: [Assistir no YouTube](https://youtu.be/60Ev5qUVokM)
   - Google Colab: [Open in Colab](https://colab.research.google.com/github/renatoruiz2607/fiapCursoTecIA/blob/dev/fase6/cap1/fiapAgroNeuralNetwork/RenatoRuiz_rm572235_pbl_fase6.ipynb)

- <b>Explicação de decisões técnicas</b>:
   - O projeto utiliza PyTorch e TensorFlow/Keras para explorar duas abordagens distintas de Visão Computacional: detecção e localização de objetos com YOLOv5 e classificação de imagens com CNN.
   - As imagens foram divididas em 74 para treinamento, 10 para validação e 10 para teste, separando os dados utilizados no aprendizado daqueles empregados na avaliação final dos modelos.
   - O conjunto de teste foi organizado com 5 imagens de cada classe, permitindo avaliar o desempenho individual dos objetos sem favorecer uma categoria pela quantidade de amostras.
   - A comparação com o YOLO padrão permite evidenciar a importância do fine-tuning, especialmente porque a classe controle PS5 não corresponde a uma categoria específica reconhecida pelo modelo original.
   - A CNN foi construída do zero, sem transferência de aprendizado, para avaliar a capacidade de uma arquitetura própria aprender características visuais das duas classes a partir das imagens disponíveis.
   - A CNN utiliza três camadas convolucionais, com 32, 64 e 128 filtros, permitindo extrair características visuais progressivamente mais complexas.
   - As camadas de MaxPooling foram utilizadas para reduzir as dimensões espaciais das representações, diminuindo o custo computacional e preservando características relevantes.
   - O GlobalAveragePooling2D foi adotado antes das camadas densas para reduzir a quantidade de parâmetros em comparação com uma operação de achatamento convencional (Flatten).
   - A camada Dropout de 30% foi incluída como mecanismo de regularização, buscando reduzir o risco de overfitting durante o treinamento da CNN.
   - A camada de saída da CNN utiliza Softmax com dois neurônios, permitindo calcular as probabilidades de classificação entre controle PS5 e garrafa térmica.
   - O otimizador Adam, com taxa de aprendizado de 0,001, foi utilizado na CNN por sua capacidade de ajustar adaptativamente os parâmetros durante o treinamento.
   - As imagens da CNN foram redimensionadas para 128 × 128 pixels, reduzindo o custo computacional e padronizando as entradas da rede neural.
   - O treinamento da CNN foi configurado com 30 épocas e batch size de 8, permitindo avaliar uma arquitetura relativamente simples em condições compatíveis com o tamanho reduzido do dataset.
   - A avaliação do YOLO utilizou Precision, Recall, mAP@0.5 e mAP@0.5:0.95, considerando tanto a capacidade de identificar os objetos quanto a qualidade da localização por meio das bounding boxes.
   - A avaliação da CNN utilizou acurácia, Precision, Recall, F1-score e matriz de confusão, permitindo analisar os acertos e erros de classificação de cada classe.
   - A matriz de confusão foi incluída para identificar quais objetos foram classificados incorretamente, complementando as métricas gerais com uma análise dos tipos de erro.
   - O conjunto reduzido de imagens foi considerado uma limitação experimental, pois pequenas quantidades de erros podem provocar variações significativas nas métricas, especialmente no conjunto de teste com apenas 10 amostras.


## 🔧 Como executar o código

***Pré Requisitos:***

*Crie a arquitetura de pastas no Google Drive:*

dataset {
  images {
    train,
    test,
    val
  },
  labels {
    train,
    test,
    val
  }
}

*Preparar no um dataset com 40 fotos de cada objeto, separando 32 para treino, 4 para teste e 4 para validação.*

*Salve estas imagens na pasta images, separando-as nas pastas train, test e val*

*Enviar essas imagens ao MakeSense.ai, criar as classes dos objetos que quer detectar e rotulá-los de acordo.*

*Ao fim de cada grupo de imagens rotuladas, exporte as anotações (arquivos .txt) e grave na pasta referente ao grupo dentro da pasta labels*

***Funcionamento:***

*Abrir o arquivo `RenatoRuiz_rm572235_pbl_fase6.ipynb`*

*Clicar no botão `Open in Colab`*

*Após isso, no conteúdo principal, cada bloco de código contém um botão executar*

*Vá executando todos de cima abaixo, não pule nenhum, para que tudo rode corretamente.*

*Vale lembrar que todas as descrições e análises são baseadas nas 94 imagens utilizadas e de acordo com o treinamento realizado quando o projeto foi buildado.*

*Todos os indicadores, estatísticas e valores podem mudar a cada build e a cada grupo de imagens.*


## 💵 Análise imagens e resultados

*Foi realizada uma estimativa de custos On-Demand (100% de utilização) na AWS Pricing Calculator para uma máquina Linux simples, destinada a hospedar a API que receberia os dados dos sensores e executaria o modelo de Machine Learning.*


---


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
