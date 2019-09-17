#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import os

from copy import deepcopy


# In[40]:



def votos(path):
 
 rootPath=path
 
 for root,dirs,files in os.walk(rootPath):
     t=0
     for arquivo in files:
         
         if arquivo[:2]=='LV':
                     
             file=os.path.join(rootPath,arquivo)

             df=pd.read_csv(file,sep='\t',encoding='latin-1',header=None)

             nomes=[]
             partido=[]
             voto=[]
             codigo=[]
             estado=[]

             sessao=df[0].iloc[0].split()[0]+df[0].iloc[0].split()[1]

             for k in range(len(df[0])):
 
                 nome=[]
                 resto=[]
 
                 lista=df[0].iloc[k].split()
 
                 if '<------->' in lista:
                     lista[lista.index('<------->')]='Não Votou'
 
                 lista.pop(0)
                 lista.pop(0)
                 
 
                 for j in lista:
                     if j.isupper():
                         nome.append(j)
                     else:
                         resto.append(j)
                 if 'Podemos' in resto:
                     partido.append('Podemos')
                     resto.pop(resto.index('Podemos'))
                 
                 elif 'Patriota' in resto:
                     partido.append('Patriota')
                     resto.pop(resto.index('Patriota'))
                     
                 elif resto[1][0:10]=='Solidaried':
                     resto[1]=resto[1].replace('Solidaried','')
                     partido.append('Solidariedade')
     
                 elif 'Avante' in resto:
                     partido.append('Avate')
                     resto.pop(resto.index('Avante'))
                 elif 'S.Part.' in resto:
                     partido.append('S.Part.')
                     resto.pop(resto.index('S.Part.'))
                 elif 'PCdoB' in resto:
                     partido.append('PCdoB')
                     resto.pop(resto.index('PCdoB'))
 
                 else:
                     partido.append(nome[-1])
                     nome.pop(-1)
     
                 nome=' '.join(nome)
 
                 nomes.append(nome)
                 voto.append(resto[0])
                 codigo.append(int(resto[-1].strip()))
                 resto.pop(0)
                 resto.pop(-1)
 
                 estado.append(' '.join(resto))
 
             if t==0:
                 t+=1
                     
                 df_votos=pd.DataFrame()
                 df_votos['Nome']=nomes
                 df_votos['Partido']=partido
                 df_votos['Estado']=estado
                 df_votos['Codigo']=codigo
                 df_votos[sessao]=voto
                 df_votos=df_votos.sort_values(by=['Codigo'])
                 df_votos=df_votos.reset_index(drop=True)
                     
             else:
                 df_tem=pd.DataFrame()
                 df_tem[sessao]=voto
                 df_tem['Codigo']=codigo
                 df_tem=df_tem.sort_values(by=['Codigo'])
                 df_tem=df_tem.reset_index(drop=True)
                 
                 df_votos[sessao]=df_tem[sessao]
 
 return df_votos


# In[45]:


def save_votos(path,name):
    rootPath=path
    arquivo=name
    newfile=os.path.join(rootPath,arquivo)
    df=votos()
    df.to_csv(newfile,encoding='latin-1')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




