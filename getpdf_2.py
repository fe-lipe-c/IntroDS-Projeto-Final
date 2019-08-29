#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import os,os.path,sys

from tika import parser

import re

from copy import deepcopy


# In[2]:


def find_str(s, char):
    index = 0
    positions=[]

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    
                    positions.append(index)

            index += 1

    return positions

def find_index(lista,posicao):
    
    indice=0
    
    for i in lista:
        if posicao>i:
            indice+=1
        else:
            return indice


# In[3]:


def extractPDF_type1(path):
    
    
    file_data=parser.from_file(path)
    text=file_data['content']
    
    ret=text.split('Sessão de:')[1].split('DOS DEPUTADOS')[0]
    retirar='Sessão de:'+ret+'DOS DEPUTADOS'
    text=text.replace(retirar,'')
    
    sessoes_dict={}
    
    text=text.replace('SRA','SR')
    
    posicoes_fala=find_str(text,'SR')
    
    momentos_da_sessao=['ABERTURA DA SESSÃO','LEITURA DA ATA','EXPEDIENTE','PEQUENO EXPEDIENTE','GRANDE EXPEDIENTE',                       'COMUNICAÇÕES PARLAMENTARES','ENCERRAMENTO','BREVES COMUNICAÇÕES','ORDEM DO DIA']
    
    for momento in momentos_da_sessao:
        
        pos_nivel=find_str(text,momento)
        if len(pos_nivel)>0:
            
            i_momento=find_index(posicoes_fala,pos_nivel[0])
            sessoes_dict[momento]=i_momento
    
    erro=[]
    discursos=text.split('SR.')
    
    for i in range(0,len(discursos)):
        
        nome_dep=discursos[i].split('(')[0].replace('.','').strip()
        if len(nome_dep)>5:
            
            if nome_dep[-5:]=='BLOCO':
            
                nome_dep=nome_dep[:-6]
            
        n_pres=[]
        if nome_dep=='PRESIDENTE':
            
            nome_presidente=discursos[i].split('(')[1].split(')')[0].replace('-',' ').replace('/',' ').replace('.','').split()
            
            for k in nome_presidente:
                if not k.isupper():
                    n_pres.append(k)
                    
            nome_dep=(' '.join(n_pres)).upper()
            
        
            
        
        try:
            
            if len(n_pres)==0:
                sessoes_dict[nome_dep].append([i,'DEPUTADO',discursos[i].split(') ')[1]])
            
            else:
                sessoes_dict[nome_dep].append([i,'PRESIDENTE',discursos[i].split(') ')[1]])
            
        
        except:
            try:
                
                if len(n_pres)==0:
                    
                    partido_estado=discursos[i].split('(')[1].split(')')[0].replace('-',' ').replace('/',' ').replace('.','').split()
                    part_est=[]
                    for j in partido_estado:
                        if j.isupper():
                            part_est.append(j)
                
                
                    sessoes_dict[nome_dep]=part_est
                    sessoes_dict[nome_dep].append([i,'DEPUTADO',discursos[i].split(') ')[1]])
                    
                else:
                    partido_estado=discursos[i].split('(')[1].split(')')[0].replace('-',' ').replace('/',' ').replace('.','').split()
                    part_est=[]
                    for j in partido_estado:
                        if j.isupper():
                        
                            part_est.append(j)
                
                
                    sessoes_dict[nome_dep]=part_est
                    sessoes_dict[nome_dep].append([i,'PRESIDENTE',discursos[i].split(') ')[1]])
                    
                    
            except:
                erro.append(i)
    
    
    sessao_legislativa=text.split('REDAÇÃO')[1].split('SESSÃO')[0].replace('\n','').strip()[:-1]
    legislatura=text.split('INÁRIA DA')[1].split('LEGISLATURA')[0].replace('\n','').strip()[:-1]
    sessao=(text.split('LEGISLATURA')[1].split('SESSÃO')[0]).replace('\n','').strip()[:-1]
    sessoes_dict['Sessão Legislativa']=sessao_legislativa
    sessoes_dict['Legislatura']=legislatura
    sessoes_dict['Sessão']=sessao
    sessoes_dict['Data']=path.split('Data2\\')[1].split('.pdf')[0].split('_')[0:3]
    sessoes_dict['Hora']=path.split('Data2\\')[1].split('.pdf')[0].split('_')[-1]
    sessoes_dict['Tipo']=path.split('Data2\\')[1].split('.pdf')[0].split('_')[3:-1]
    
    
    
    return sessoes_dict


# In[6]:


#path=r'D:\EMAP\Fundamentos Data Science\Data2'
#file='2019_7_12_Sessão_Extraordinária__0931.pdf'
#file2='2018_9_4_Sessão_Extraordinária__0931.pdf'
#file3='2019_4_17_Sessão_Solene__0930'
#filename=os.path.join(path,file)
#filename2=os.path.join(path,file2)
#filename3=os.path.join(path,file3)


# In[4]:


def agregar_dict(ano):
    rootPath=r'D:\EMAP\Fundamentos Data Science\Data2'
    arq=[]
    dicionarios=[]
    
    for root,dirs,files in os.walk(rootPath):
        for arquivo in files:
            if arquivo[0:4]==ano:
                
                if 'Solene' in arquivo.split('Sessão_')[1].split('.pdf')[0].split('_'):
                    continue
                elif 'Congresso' in arquivo.split('Sessão_')[1].split('.pdf')[0].split('_'):
                    continue
                else:
                    arq.append(arquivo)
                    
    
    for file in arq:
        
        filename=os.path.join(rootPath,file)
        sessao_dict=extractPDF_type1(filename)
        
        dicionarios.append(sessao_dict)
        
    return dicionarios
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[48]:


def discurso_concatenado(sessao):
    
    partido_dep=[]
    discurso=[]
    estado_dep=[]
    palavras_deputados=[]
    nome=[]
    ordem_da_fala=[]
    cargo=[]
    bancada=[]
    
    dic_dis={}
    dic_qtd={}
    
    GOVERNO=['PSL','PP','PSD','MDB','PR','PRB','DEM','PSDB','PTB','PMN','PSC','NOVO','PTC','PHS']
    BLOCO_A=['PDT','AVANTE','PATRI','PV','PROS','PPS','CIDADANIA','SOLIDARIEDADE','PODE','PL','DC','PRP','PATRIOTA']
    OPOSICAO=['PT','PSOL','PSB','REDE','PCdoB','PPL']

    for i in sessao.keys():
        
        if i=='IRACEMA PORTELLA':
            continue
            
        if i=='OSSESIO SILVA':
            continue
            
        if i=='MAGDA MOFATTO':
            continue
            
        if i=='MARCIO ALVINO':
            continue
            
        if i=='DANRLEI DE DEUS HINTERHOLZ':
            continue
        
        if i=='BIA CAVASSA':
            continue
            
            
        if i=='':
            
            deputado=sessao.get(i)
            partido='PSB'
            estado='AL'
            partido_dep.append(partido)
            estado_dep.append(estado)
            qtd_palavras=0
            concatenado=''
            o_fala=[]
            nome.append('JHC')
            
            dic_dis['JHC']=[]
            dic_qtd['JHC']=[]
            for j in range(3,len(deputado)):
                qtd_palavras=qtd_palavras+len(deputado[j][2].split())
                concatenado=concatenado+' '+deputado[j][2]
                o_fala.append(deputado[j][0])
                dic_dis['JHC'].append(deputado[j])
                dic_qtd['JHC'].append(len(deputado[j][2].split()))
                
            palavras_deputados.append(qtd_palavras)
            discurso.append(concatenado)
            ordem_da_fala.append(o_fala)
            bancada.append('OPOSIÇÃO')
                
            continue
            
            
    
        if i[0:4]=='Sess':
            continue
    
        deputado=sessao.get(i)
    
        if str(deputado).isnumeric():
            continue
    
        if len(deputado)<3:
            
            try:
                if str(deputado[1][0]).isnumeric():
                    
                    partido='PCdoB'
                    estado=deputado[0]
                    partido_dep.append(partido)
                    estado_dep.append(estado)
                    qtd_palavras=0
                    concatenado=''
                    o_fala=[]
                    nome.append(i)
                    
                    dic_dis[i]=[]
                    dic_qtd[i]=[]
                    for j in range(1,len(deputado)):
                        qtd_palavras=qtd_palavras+len(deputado[j][2].split())
                        concatenado=concatenado+' '+deputado[j][2]
                        o_fala.append(deputado[j][0])
                        dic_dis[i].append(deputado[j])
                        dic_dis[i].append(deputado[j])
                        dic_qtd[i].append(len(deputado[j][2].split()))
                        
                    palavras_deputados.append(qtd_palavras)
                    discurso.append(concatenado)
                    ordem_da_fala.append(o_fala)
                    bancada.append('OPOSIÇÃO')
                
                    continue
            except:
                
                continue
        
        partido=deputado[0]
        
            
        
        if partido.isnumeric() or partido=='Sessão':
            continue
        
        
        estado=deputado[1]
        
        
        if str(deputado[1][0]).isnumeric():
            
                    
            partido='PCdoB'
            estado=deputado[0]
            partido_dep.append(partido)
            estado_dep.append(estado)
            qtd_palavras=0
            concatenado=''
            o_fala=[]
            nome.append(i)
            dic_dis[i]=[]
            dic_qtd[i]=[]
            
            for j in range(1,len(deputado)):
                qtd_palavras=qtd_palavras+len(deputado[j][2].split())
                concatenado=concatenado+' '+deputado[j][2]
                o_fala.append(deputado[j][0])
                dic_dis[i].append(deputado[j])
                
                dic_qtd[i].append(len(deputado[j][2].split()))
                
            palavras_deputados.append(qtd_palavras)
            discurso.append(concatenado)
            ordem_da_fala.append(o_fala)
            bancada.append('OPOSIÇÃO')
                
            continue
            
        if partido in GOVERNO:
            
            bancada.append('GOVERNO')
            
        elif partido in OPOSICAO:
            bancada.append('OPOSIÇÃO')
            
        elif partido in BLOCO_A:
            
            bancada.append('BLOCO_A')
            
        else:
            print('deputado ',i,' err')
            print('ERRO: ',partido)
            print(deputado)
            
        partido_dep.append(partido)
        estado_dep.append(estado)
    
        if len(deputado[2])<3:
            continue
        
    
        qtd_palavras=0
        concatenado=''
        
        o_fala=[]
        nome.append(i)
        dic_dis[i]=[]
        dic_qtd[i]=[]
        
        for j in range(2,len(deputado)): # quantidade de palavras ditas
            
           
            try:
                
                qtd_palavras=qtd_palavras+len(deputado[j][2].split())
                concatenado=concatenado+' '+deputado[j][2]
                o_fala.append(deputado[j][0])
                dic_dis[i].append(deputado[j])
                
                dic_qtd[i].append(len(deputado[j][2].split()))
                
            except:
                print(dic_dis)
                print(i)
                print(j)
                return deputado
            
        
        palavras_deputados.append(qtd_palavras)
        discurso.append(concatenado)
        ordem_da_fala.append(o_fala)
        
    df=pd.DataFrame(nome,columns=['Nome'])
    df['Partido']=partido_dep
    df['Bancada']=bancada
    df['Estado']=estado_dep
    df['Discurso']=discurso
    df['Quantidade']=palavras_deputados
    df['Ordem']=ordem_da_fala
    
    
    return df,discurso,dic_dis,dic_qtd


# In[ ]:





# In[ ]:





# In[6]:


def dict_of_dicts_merge(x, y):
    z = {}
    overlapping_keys = list(x.keys() & y.keys())
    
    
    for key in overlapping_keys:
        if str(key).isnumeric():
            
            continue
        if str(y[key]).isnumeric() or str(x[key]).isnumeric():
            
            continue
        
        lista1=deepcopy(x[key])
        lista2=deepcopy(y[key])
        try:
            
            lista1.extend(lista2[2:])
        
            z[key] = lista1
        except:
            print(key)
            pass
    x_keys=[item for item in x.keys() if item not in overlapping_keys]
    y_keys=[item for item in y.keys() if item not in overlapping_keys]
    for key in x_keys:
        z[key] = deepcopy(x[key])
    for key in y_keys:
        z[key] = deepcopy(y[key])
    return z


# In[ ]:





# In[7]:


def ultimato(tudo):
    
    dicionar=deepcopy(tudo[0])

    for indice in range(1,len(tudo)):
    
        dicionar=dict_of_dicts_merge(dicionar,tudo[indice])
    
    return dicionar
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




