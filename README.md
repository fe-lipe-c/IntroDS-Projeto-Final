# Projeto Final
Projeto final para a disciplina de Fundamentos de Data Science, da Escola de Matemática Aplicada - EMAP/FGV

## Lista de Pastas e Arquivos
### Pastas

* **Papers**: alguns artigos que foram ou não utilizados como referência para realizar o projeto.
* **Versões**: _jupyter notebooks_ com códigos-pilotos para extrair os dados do site da Câmara dos Deputados.

  - **Untitled.ipynb**: (abandonado) código para extrair o texto dos arquivos pdf.
  - **ftlog.log** e **ftlog_dias_sessao.log**: log das mensagens de erro para as tentativas de extrair os dados do site da Câmara dos 
    Deputados.
  - **scrape**(r)**_teste**(_2_,_3_)**.ipynb** e **cam_scrape.py**: algumas gerações de código para extrair os discursos do site da Cãmara 
    dos Deputados. O mesmo discurso está distribuido de várias formas no site. Cada um desses códigos é uma tentativa de extrair os dados 
    utilizando algum desses caminhos.
    
* **Versões_database**: algumas gerações abandonadas de códigos para implementar a base de dados.

  - **getpdf.ipynb**: código-teste verificar como extrair os discursos do pdf e uma tentativa frustrada de visualizar a quantidade de 
    palavras por discurso, na ordem cronológica.
  
* **Dados**: dados que serão utilizados no trabalho.

  - **5X-LEG-**: arquivos que contém os resultados das votações realizadas em plenário.
  - **Layout.pdf**: esquema dos arquivos 5X-LEG-.

### Arquivos

* **Dias_com_sessao.txt**: lista dos dias em que houve pelo menos uma sessão no plenário. O código em _dias_sessao.ipynb_ gera esse arquivo,
  utilizando a biblioteca Pickle.
* **Sessões-parte18-19.zip**: amostra de algumas sessões de 2018 e 2019.
* **dias_sessao.ipynb**: código para baixar os dias em que houve pelo menos uma sessão no plenário. 
* **scrape_teste4.ipynb**: código para extrair os discursos dos deputados do site da Câmara dos Deputados.
