#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import getpdf_2
import get_votos

import os


# In[2]:


def base_sessoes(ano):
    
    sessoes=getpdf_2.agregar_dict(ano)
    
    df=pd.DataFrame()
    momentos_da_sessao=['ABERTURA DA SESSÃO','LEITURA DA ATA','EXPEDIENTE','PEQUENO EXPEDIENTE','GRANDE EXPEDIENTE',                       'COMUNICAÇÕES PARLAMENTARES','ENCERRAMENTO','BREVES COMUNICAÇÕES','ORDEM DO DIA']
    
    
    for p in range(len(sessoes)):
        
        sessao=sessoes[p]

        fases=[(0,'')]
        
        for j in sessao.keys():
            
            if str(sessao[j]).isnumeric():
                if j.isupper():
                    fases.append((sessao[j],j))
        
        fases=sorted(fases)
        
        fases2=fases.copy()
        fases=[]
        for f in range(1,len(fases2)):
            if (fases2[f][0]-fases2[f-1][0])==0:
                fases2[f-1]=(-1,fases2[f-1][1])
        
        fases2=sorted(fases2)        
        for f in fases2:
            if f[0]>-1:
                fases.append(f)
        
        for i in sessao.keys():
            if sessao[i] is None:
                continue
    
            if str(sessao[i]).isnumeric():
                continue
        
            else:
                if len(sessao[i])==0:
                    continue
                if i=='Data':
                    continue
                if i =='Tipo':
                    continue
        
                if i[:6]=='Sessão':
                    continue
                
                for k in sessao[i][2:]:
                    
                    if len(k)<3:
                        print('Sessao: ',p)
                        print('Key: ', i)
                        continue
                        
                    t=0
                    h=1
                    f_k=''
                    try:
                        
                        while t==0:
                        
                            if h==len(fases):
                            
                                t+=1
                           
                                f_k=fases[h-1][1]
                        
                            elif int(k[0])>=int(fases[h-1][0]) and int(k[0])<=int(fases[h][0]):
                                t+=1
                            
                                f_k=fases[h-1][1]
                            
                            h+=1
                    except:
                        print(k,p)
                        
                    df=df.append({'Nome':i,'Data':sessao['Data'],'Sessão Legislativa':sessao['Sessão Legislativa'],                                 'Legislatura':sessao['Legislatura'],'Sessão':sessao['Sessão'],'Hora':sessao['Hora'],                                 'Tipo':sessao['Tipo'],'Partido':sessao[i][0],'Estado':sessao[i][1],'Ordem':str(k[0]),                                  'Presidente':k[1],'Discurso':k[2],'Fase':f_k},ignore_index=True)
        
    return df


# In[9]:


def save_discursos(rootPath,arquivo,df_discursos):
    newfile=os.path.join(rootPath,arquivo)
    df_discursos.to_csv(newfile,encoding='utf-8')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




