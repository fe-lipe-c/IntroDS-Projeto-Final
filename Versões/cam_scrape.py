#!/usr/bin/env python
# coding: utf-8

# In[4]:


import time
from selenium import webdriver


# In[136]:


def scrape(inicio=56591):
    
    browser=webdriver.Firefox()
    url1='https://www.camara.leg.br/internet/escriba/escriba.asp?codSileg={0}'.format(inicio)
    browser.get(url1)
    iframe=browser.find_element_by_xpath('//*[@id="ifrmEscriba"]')
    browser.switch_to.frame(iframe)
    Sessoes=[]
    Verificar=[]
    
    for i in range(56591,56561,-1):
        try:
            temp={}
            url='https://www.camara.leg.br/internet/escriba/escriba.asp?codSileg={0}'.format(i)
            browser.get(url)
            iframe=browser.find_element_by_xpath('//*[@id="ifrmEscriba"]')
            browser.switch_to.frame(iframe)
            
            sessao=browser.find_element_by_xpath('/html/body/div/div[1]/div/strong[3]').text
            data=browser.find_element_by_xpath('/html/body/div/div[1]/div/span[1]/span').text
            tipo=browser.find_element_by_xpath('/html/body/div/div[1]/div/strong[4]').text
            
            tudo='//*[@id="contentEncontro"]'
            temp['Sessao']=sessao
            temp['Data']=data
            temp['Tipo']=tipo
            temp['Pagina']=i
            
            temp['Conteudo']=browser.find_element_by_xpath(tudo).text
            
            Sessoes.append(temp)
            
        except:
            
            try:
                browser.find_element_by_xpath('/html/body/div/h1').text
            except:
                Verificar.append(i)
        
    
    return Sessoes,Verificar


# In[ ]:


if __name__=='__main__':
    import sys
    scrape(str(sys.argv[1]))


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





# In[ ]:




