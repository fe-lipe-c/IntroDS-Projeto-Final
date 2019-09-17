#!/usr/bin/env python
# coding: utf-8

# In[61]:


import numpy as np
import pandas as pd

import base_dados_2

import os,sys

import gensim
from gensim import corpora
from gensim.models import ldamodel
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet


import spacy

import itertools
from itertools import islice
import random
import pyLDAvis
import pyLDAvis.gensim
from IPython.display import Image

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import re

from pprint import pprint

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
get_ipython().run_line_magic('matplotlib', 'inline')

#pwd
#ls
import seaborn as sns


from sklearn.manifold import TSNE

import altair as alt
alt.renderers.enable('notebook')

import logging 

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=None)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
rootLogger.propagate = False

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)




# In[3]:


def norm_discursos():
    
    mydir=os.getcwd()
    
    df19=base_dados_2.base_sessoes('2019',mydir)
    df19[df19['Fase']!='ABERTURA DA SESSÃO']['Fase'].unique()
    df_=df19[df19['Fase']!='ABERTURA DA SESSÃO']
    df_=df_[df_['Fase']!='EXPEDIENTE']
    df_=df_[df_['Fase']!='LEITURA DA ATA']
    df_=df_[df_['Presidente']=='DEPUTADO'].reset_index(drop=True)
    dados=df_.Discurso.values.tolist()
    df_teste=df_
    df_teste['Discurso']=df_.Discurso.values.tolist()
    dados2=[]
    dados3=pd.DataFrame()
    for j,i in enumerate(df_teste['Discurso']):
        if len(i)>100:
            dados2.append(i)
            dados3=dados3.append(df_teste.iloc[j],ignore_index=True)
    dados2 = [re.sub('\s+', ' ', sent) for sent in dados2]
    
    def discurso_para_palavras(discursos):
    
        for fala in discursos:
            yield(gensim.utils.simple_preprocess(str(fala),deacc=True))
            
    dados_p=list(discurso_para_palavras(dados2))
    
    bigram=gensim.models.Phrases(dados_p,min_count=20,threshold=50)
    trigram=gensim.models.Phrases(bigram[dados_p],threshold=50)
    bigram_mod=gensim.models.phrases.Phraser(bigram)
    trigram_mod=gensim.models.phrases.Phraser(trigram)
    
    StopWords=set(stopwords.words('portuguese'))
    add_stopwords=['tambem','registrar','discursar','gostar','agradeco','seguir','presidente','sr','partir','tempo','orientar',               'destacar','nome','srs','deputados','lider','minoria','iniciar','estar','sao','sessao','encerrar','julho',               'falar','nao','fazer','aqui','querer','dizer','ja','dar','agora','sim','destaque','art','hoje','estar',               'falar','dizer','voces','sra','exa','ainda','dizer','contar','saber','ficar','deixar','passar','deliberativa',               'estao','ser','nº','cd','extraordinaria','partir']
    for word in add_stopwords:
        StopWords.add(word)
    
    def remove_stopwords(texto):
        return [[palavra for palavra in simple_preprocess(str(doc)) if palavra not in StopWords] for doc in texto]

    def make_bigrams(texto):
        return [bigram_mod[doc] for doc in texto]

    def make_trigrams(texto):
        return [trigram_mod[bigram_mod[doc]] for doc in texto]
    
    def lemmatization(texto,tags=['NOUN','ADJ','VERB','ADV']):
        texto_out=[]
        for sent in texto:
            doc=nlp(' '.join(sent))
            texto_out.append([token.lemma_ for token in doc if token.pos_ in tags])
        return texto_out
    
    dados_p_nosw=remove_stopwords(dados_p)
    dados_p_bigrams=make_bigrams(dados_p_nosw)
    dados_p_trigrams=make_trigrams(dados_p_nosw)
    nlp=spacy.load('pt_core_news_sm',disable=['parser','ner'])
    dados_p_lem=lemmatization(dados_p_bigrams,tags=['NOUN','ADJ','VERB','ADV'])
    dados_p_lem_nosw=remove_stopwords(dados_p_lem)
    dados_dict=corpora.Dictionary(dados_p_lem_nosw)
    dados_dict.filter_extremes(no_below=20, no_above=0.3)
    textos=dados_p_lem_nosw
    corpus=[dados_dict.doc2bow(text) for text in textos]
    
    return dados2,corpus,dados_dict,dados_p_lem_nosw


# In[ ]:


def LDA_discursos(corpus,dados_dict,topicos,dados_p_lem_nosw):
    logging.disable(logging.CRITICAL)
    lda_model=gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=dados_dict,num_topics=topicos,random_state=100,update_every=1,                                         chunksize=100,passes=10,alpha='auto',per_word_topics=True)
    pprint(lda_model.print_topics())
    doc_lda=lda_model[corpus]
    
    coherence_model_lda=CoherenceModel(model=lda_model,texts=dados_p_lem_nosw,dictionary=dados_dict,coherence='c_v')
    coherence_lda=coherence_model_lda.get_coherence()
    print('\nCoherence Score: ',coherence_lda)
    
    return lda_model


# In[131]:


def compute_coherence_values(dic,corpus,texts,limit,start=2,step=3):
    logging.disable(logging.CRITICAL)
    coherence_values=[]
    model_list=[]
    for num_topics in range(start,limit,step):
        model=gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=dic,num_topics=num_topics,random_state=100,update_every=1,                                         chunksize=100,passes=5,alpha='auto',per_word_topics=True)
        model_list.append(model)
        coherencemodel=CoherenceModel(model=model, texts=texts, dictionary=dic, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        coherence_lda=(num_topics,coherencemodel.get_coherence())
        
        print('\nCoherence Score: ',coherence_lda)
        
    plt.plot(coherence_values)    
    return model_list, coherence_values,coherence_lda


# In[28]:


#pyLDAvis.enable_notebook()
#vis = pyLDAvis.gensim.prepare(lda_model, corpus, dados_dict)
#vis


# In[29]:





# In[262]:


def format_topics_sentences(texts,ldamodel, corpus):
    sent_topics_df = pd.DataFrame()

    for i, row in enumerate(ldamodel[corpus]):
        ranking = sorted(row[0], key=lambda x: x[1], reverse=True)
        
        for j, (topic_num, prop_topic) in enumerate(ranking):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Tópico_Dominante', 'Contribuição', 'Palavras-chave']

    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


# In[ ]:





# In[ ]:





# In[ ]:




