# Projeto Final
Projeto final para a disciplina de Fundamentos de Data Science, da Escola de Matemática Aplicada - EMAP/FGV

### Equipe

Felipe Costa

Maria Gabriela Gontijo

### Objetivo

Através dos discursos e do padrão de votos dos membros da Câmara dos Deputados, inferir os tópicos mais relevantes e como cada deputado e cada partido votam.
De forma mais precisa, este trabalho se propõe a responder as seguintes questões: i) os deputados votam de acordo com o partido ou de acordo com o estado que representa? ii) quais deputados são mais presentes nas sessões? iii) quais temas são mais abordados nas sessões? iv) qual tema é mais abordado por cada partido?

### Utilizando os códigos

Existem dois arquivos na pasta principal deste repositório: Analise_camara_dos_deputados.ipynb e analise_discursos.ipynb. O primeiro tem duas partes, a primeira dedicada à modelagem dos tópicos e a segunda a inferência sobre o padrão de votos dos deputados. O segundo jupyter notebook se concentra em uma análise mais minuciosa dos dados, escolhendo players de destaque para o escrutínio. O restante dos arquivos presentes nas outras pastas servem como suporte para o bom funcionamento desses códigos.

### Sobre os dados

Os dados foram coletados no site da Câmara dos Deputados e são compostos por discursos e contabilização de votos. Para isso foi utilizado o arquivo scrape_teste4.ipynb
  
* **Dados**: dados que serão utilizados no trabalho.

  - **5X-LEG-**: arquivos que contém os resultados das votações realizadas em plenário.
  - **Sessões-parte18-19.zip**: sessões em plenário de 2018 e de 2019.

### Requisitos
Para instalar as bibliotecas abaixo, foi utilizado o software Anaconda.
* **tika**: conda install -c conda-forge tika (extração de dados de documentos em pdf)
* **spacy**: conda install -c conda-forge spacy (biblioteca de NLP)
* **spacy**: conda install -c conda-forge spacy-model-pt_core_news_sm (utilizado para 'lematization')
* **pyLDAvis**: conda install -c conda-forge pydavis (visualização dos tópicos gerados por LDA)
* **Wordcloud**: conda install -c conda-forge wordcloud
* **Altair**: conda install -c conda-forge altair (visualizações interativas)
* **gensim**: conda install -c anaconda gensim

Caso não possua o Anaconda, segue o link:https://www.anaconda.com/distribution/





         
         
* 
