#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
import os,sys
import numpy as np

import get_votos

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.manifold import TSNE

import altair as alt
alt.renderers.enable('notebook')

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import networkx as nx
import chart_studio

import time


# In[13]:


def lado_partido(df_mes):
    
    GOVERNO=['PSL','PP','PSD','MDB','PR','PRB','DEM','PSDB','PTB','PMN','PSC','NOVO','PTC','PHS']
    MINORIA=['PDT','AVANTE','Avate','PATRI','PV','PROS','PPS','CIDADANIA','SOLIDARIEDADE','Solidariedade',             'PODE','PL','DC','PRP','PATRIOTA','Patriota','Podemos','S.Part.']
    OPOSICAO=['PT','PSOL','PSB','REDE','PCdoB','PPL']
    df_mes['Lado']=0
    for i in range(len(df_mes['Partido'])):
        if df_mes['Partido'].iloc[i] in GOVERNO:
            df_mes['Lado'].iloc[i]='GOVERNO'
        elif df_mes['Partido'].iloc[i] in OPOSICAO:
            df_mes['Lado'].iloc[i]='OPOSIÇÃO'
        elif df_mes['Partido'].iloc[i] in MINORIA:
            df_mes['Lado'].iloc[i]='MINORIA'
        else:
            print(df_mes['Partido'].iloc[i])
            print(i)


# In[36]:


def matriz_votos(df_mes):
    
    mat_vts=np.zeros((len(df_mes),len(df_mes.iloc[:,4:-1].columns)))
    num_votes_in_row=np.zeros(len(df_mes))
    
    for linha in range(len(df_mes)):
        num_votes = 0
        votos = df_mes.loc[[linha]].iloc[:,4:-1]
        roll_array = np.zeros(len(votos.columns))
        for idx,vt in enumerate(votos.columns):
        
            if votos[vt].iloc[0]=='Sim':
                roll_array[idx] = 1
                num_votes = num_votes + 1
            elif votos[vt].iloc[0]=='Não':
                roll_array[idx] = -1
                num_votes = num_votes + 1
            elif votos[vt].iloc[0]=='Obstrução':
                roll_array[idx] = -1
                num_votes = num_votes + 1  
            elif votos[vt].iloc[0]=='Abstenção':
                roll_array[idx] = 0
                num_votes = num_votes + 1
            else:
                roll_array[idx] = 0
        num_votes_in_row[linha] = num_votes

        mat_vts[linha] = roll_array
    
    return mat_vts,num_votes_in_row


# In[45]:


def tsne_(mes):
    mydir=os.getcwd()
    mydir=mydir.replace('\\Scripts','')+'\\Data3'
    
    if mes=='fevereiro':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Fevereiro19'.format(mydir)
    elif mes=='marco':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Março19'.format(mydir)
    elif mes=='abril':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Abril19'.format(mydir)
    elif mes=='maio':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Maio19'.format(mydir)
    elif mes=='junho':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Junho19'.format(mydir)
    elif mes=='julho':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Julho19'.format(mydir)
    elif mes=='agosto':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Agosto19'.format(mydir)
    elif mes=='todos':
        path=mydir+'Todos os meses'
        path=r'{0}\Todos os meses'.format(mydir)
        
    else:
        print('Erro: mês não encontrado.')
    print(path)
    vt_todos=get_votos.votos(path)
    lado_partido(vt_todos)
    matriz,arr=matriz_votos(vt_todos)
    
    tsne=TSNE()
    tsne_vt=tsne.fit_transform(matriz)
    vt_todos['tsne-1d-one']=tsne_vt[:,0]
    vt_todos['tsne-2d-two']=tsne_vt[:,1]
        
    xscale = alt.Scale(domain=(-45, 45))
    yscale = alt.Scale(domain=(-40, 40))
    
    chart=alt.Chart(vt_todos,width=700,height=400).mark_point(size=45).encode(alt.X('tsne-1d-one',scale=xscale),                                                                        alt.Y('tsne-2d-two',scale=yscale),color='Lado',                                                                        tooltip=['Nome','Partido','Estado']).properties(title='Votos - 2019')
    
    chart_part=alt.Chart(vt_todos,width=250,height=100).mark_point(size=10).encode(x='tsne-1d-one:Q',y='tsne-2d-two:Q'                                                                  ,color='Lado:N',                             
                                                                  tooltip=['Nome','Partido','Estado'],\
                                                                  facet='Partido:O').properties(columns=4,width=200,height=100)
    
    chart.display()
    chart_part.display()


# In[ ]:





# In[47]:


def rede_est_part(df_pe):
    print('Fase 0')
    deputados = df_pe['Nome']
    pesos= {dep:{ped: 0 for ped in deputados if ped!=dep} for dep in deputados}
    
    for a in range(len(df_pe)):
        estado1=df_pe['Estado'].iloc[a]
        for b in range(a+1,len(df_pe)):
            estado2=df_pe['Estado'].iloc[b]
            if estado1==estado2:
                pesos[df_pe['Nome'].iloc[a]][df_pe['Nome'].iloc[b]]+=1
    
    for a in range(len(df_pe)):
        estado1=df_pe['Partido'].iloc[a]
        for b in range(a+1,len(df_pe)):
            estado2=df_pe['Partido'].iloc[b]
            if estado1==estado2:
                pesos[df_pe['Nome'].iloc[a]][df_pe['Nome'].iloc[b]]+=1

    g = nx.Graph()
    for par,nome in enumerate(deputados):
        g.add_node(nome)
        if df_pe['Lado'].iloc[par]=='GOVERNO':
            g.node[nome]['color'] ='b'
        elif df_pe['Lado'].iloc[par]=='OPOSIÇÃO':
            g.node[nome]['color'] ='r'
        elif df_pe['Lado'].iloc[par]=='MINORIA':
            g.node[nome]['color'] ='y'
        else:
            g.node[nome]['color'] ='m'
   
    for dep1, vizinho in pesos.items():
        for dep2, peso in vizinho.items():
            if peso == 0:
                continue
            g.add_edge(dep1,dep2, weight= peso, difference = 1. / peso)
            
    return g


# In[ ]:





# In[ ]:





# In[53]:


def mst_votes(votes_net_mes,nomes_dep=True,labels='all'):
    
    plt.figure(figsize=(30, 20))
    np.random.seed(5)
    mst = nx.minimum_spanning_tree(votes_net_mes, weight='difference')
    pos = nx.spring_layout(mst, iterations=900, k=.008, weight='difference')


    mst_edges = list(nx.minimum_spanning_edges(votes_net_mes, weight='difference'))

    nl = votes_net_mes.nodes()
    c = [votes_net_mes.node[n]['color'] for n in nl]


    nx.draw_networkx_edges(votes_net_mes, pos, edgelist=mst_edges, alpha=0.8)
    nx.draw_networkx_nodes(votes_net_mes, pos, nodelist = nl, node_color = c, node_size=120)

    for p in pos.values():
        p[1] += .02
    
    if nomes_dep==True:
        if labels=='all':
            
            nx.draw_networkx_labels(votes_net_mes, pos, font_color='k', font_size=10)
        else:
            nx.draw_networkx_labels(votes_net_mes, pos,labels, font_color='k', font_size=8)
        
    plt.title("MST of Vote Disagreement", fontsize=12)
    plt.xticks([])
    plt.yticks([])
    #remove_border(left=False, bottom=False)
    
    return mst


# In[ ]:





# In[56]:


def maj_camara(mes,resultado_prev=0,rounds='all'):
    
    mydir=os.getcwd()
    mydir=mydir.replace('\\Scripts','')+'\\Data3'
    
    if mes=='fevereiro':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Fevereiro19'.format(mydir)
    elif mes=='marco':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Março19'.format(mydir)
    elif mes=='abril':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Abril19'.format(mydir)
    elif mes=='maio':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Maio19'.format(mydir)
    elif mes=='junho':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Junho19'.format(mydir)
    elif mes=='julho':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Julho19'.format(mydir)
    elif mes=='agosto':
        path=r'{0}\56-LEG-PRIMEIRA-SESSAO-LEGISLATIVA-Agosto19'.format(mydir)
    elif mes=='todos':
        path=mydir+'Todos os meses'
        path=r'{0}\Todos os meses'.format(mydir)
        
    else:
        print('Erro: mês não encontrado.')
    print(path)
    vt_todos=get_votos.votos(path)
    lado_partido(vt_todos)
    rede=rede_est_part(vt_todos)
    
    df_mes=vt_todos
    
    if rounds=='all':
        rounds=len(df_mes.columns)-5
        
    deputados=df_mes['Nome']
    resultado_est= {dep:0 for dep in deputados}
    resultado_part={dep:0 for dep in deputados}
    res_iter_est=[]
    
    serie_res_est={dep:[] for dep in deputados}
    serie_res_part={dep:[] for dep in deputados}
    
    erro=[]

    pesos= {dep:{ped: 0 for ped in deputados if ped!=dep} for dep in deputados}
    
    for rodada in range(rounds):
        for sessao in df_mes.iloc[:,4+rodada:5+rodada]:
            df=df_mes[['Nome','Estado','Partido',sessao]]
            
            for i in range(len(df)):
                
                nome=df['Nome'].iloc[i]
                if nome not in resultado_est.keys():
                    resultado_est[nome]=0
                    
                if nome not in resultado_part.keys():
                    resultado_part[nome]=0
                    
                    
                votou1=df[sessao].iloc[i]
                
                if votou1=='Não Votou':
                    serie_res_part[nome].append(0)
                    serie_res_est[nome].append(0)
                    continue
                    
                elif votou1=='Art.':
                    serie_res_part[nome].append(0)
                    serie_res_est[nome].append(0)
                    continue
                    
                votos_t_est=[]
                votos_t_part=[]
                
                votos_abs_est=[]
                votos_abs_part=[]
                
                estado1=df[df['Nome']==nome]['Estado'].item()
                partido1=df[df['Nome']==nome]['Partido'].item()
                
                for edge in rede.edges(nome):
                    
                    votos_t=0
                    votos_abs=0
                    
                    dep2=edge[1]
                    estado2=df[df['Nome']==dep2]['Estado'].item()
                    partido2=df[df['Nome']==dep2]['Partido'].item()
                    
                    if dep2 not in set(df['Nome']):
                        votou2='Art.'
                        erro.append(dep2)
                    else:
                        votou2=df[df['Nome']==dep2][sessao].item()
                    
                    if votou2=='Não':
                        votos_t=0
                    elif votou2=='Sim':
                        votos_t=1
                    elif votou2=='Não Votou':
                        pass
                    elif votou2=='Art.':
                        pass
                    elif votou2=='Obstrução':
                        votos_t=0
                    elif votou2=='Abstenção':
                        votos_abs=-1
                    else:
                        pass
                        
                    if estado1==estado2:
                        votos_t_est.append(votos_t)
                        votos_abs_est.append(votos_abs)
                        
                    if partido1==partido2:
                        votos_t_part.append(votos_t)
                        votos_abs_part.append(votos_abs)
                        
                    if votou1==votou2:
                        pesos[nome][dep2]+=1
                        
                        
                media_est=np.mean(votos_t_est)
                media_part=np.mean(votos_t_part)
                
                if media_est>0.5:
                    vencedor_est='Sim'
                elif media_est<=0.5:
                    vencedor_est='Não'
                    
                if media_part>0.5:
                    vencedor_part='Sim'
                elif media_part<=0.5:
                    vencedor_part='Não'
                
                if votou1=='Abstenção':
                    if (len(votos_t_est)+len(votos_t_part))==0:
                       
                        res=1
                    else:
                        res_est=len(votos_abs_est)/len(votos_t_est)
                        res_part=len(votos_abs_part)/len(votos_t_part)
            
                    
                    if res_est>0.5:
                        resultado_est[nome]+=1
                        serie_res_est[nome].append(1)
                    else:
                        resultado_est[nome]-=1
                        serie_res_est[nome].append(-1)
                    
                    if res_part>0.5:
                        resultado_part[nome]+=1
                        serie_res_part[nome].append(1)
                    else:
                        resultado_part[nome]-=1
                        serie_res_part[nome].append(-1)
                        
                    continue
                        
                if votou1==vencedor_est:
                    resultado_est[nome]+=1
                    serie_res_est[nome].append(1)
                else:
                    resultado_est[nome]-=1
                    serie_res_est[nome].append(-1)
                    
                if votou1==vencedor_part:
                    resultado_part[nome]+=1
                    serie_res_part[nome].append(1)
                else:
                    resultado_part[nome]-=1
                    serie_res_part[nome].append(-1)
                    
                
        
        r=[(resultado_est.get(name),name) for name in resultado_est.keys()]
        
        t=0
        for i in sorted(r,reverse=True):
            
           
            t+=1
            if t==10:
                break
                
        
        t=0
        for i in sorted(r,reverse=False):
            
            
            t+=1
            if t==10:
                break
        
        res_iter_est.append(r)
        
    df=pd.DataFrame(list(resultado_est.items()),columns=['Nome','Votos'])
    df2=pd.DataFrame(list(resultado_part.items()),columns=['Nome','Votos'])
    df1=vt_todos[['Nome','Partido','Estado']]
    df3=vt_todos[['Nome','Partido','Estado']]
    
    df=df.merge(df1,on=['Nome'])
    df2=df2.merge(df3,on=['Nome'])
    
    df2['Voto']=0
    for i in range(len(df2)):
        if df2['Votos'].iloc[i]<0:
            df2['Voto'].iloc[i]='separado'
        else:
            df2['Voto'].iloc[i]='junto'
            
    df['Voto']=0
    for i in range(len(df)):
        if df['Votos'].iloc[i]<0:
            df['Voto'].iloc[i]='separado'
        else:
            df['Voto'].iloc[i]='junto'
        
    chart_part=alt.Chart(df2).mark_point().encode(x='Estado:O',y='Partido:O',size='Votos:Q',color='Voto:N',tooltip=['Nome','Partido','Estado']).properties(title='Votos Partido - 2019')
    ch_est=alt.Chart(df).mark_point().encode(x='Estado:O',y='Partido:O',size='Votos:Q',color='Voto:N',tooltip=['Nome','Partido','Estado']).properties(title='Votos Estado - 2019')
    
    chart_part.display()
    ch_est.display()


# In[ ]:





# In[ ]:




