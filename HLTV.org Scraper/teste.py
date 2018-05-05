import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import numpy as np
import pandas as pd
    

my_url = "https://www.hltv.org/stats/teams/5929/" + \
         "Space%20Soldiers"

#create a connection between the page and the client
#if we try at the direct way, the code does not works because
#the server blocked anything returning an 403 error

req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})


page_html = uReq(req).read()

#creat an BeautifulSoup object called page_soup
#constructor with 2 initial atributes( the html code and the library)
#there are different kind of parser libraries each one has different speed
#and different ways to parse a document
page_soup = soup(page_html, "html.parser")


#grabs each columns where are the values that I need
containers = page_soup.findAll("div",{"class":"large-strong"})


values = []


#recebe uma string, retira os elementos / e " ", a quebra num vetor

def test_bar(container):
    if "/" in container:
        container = container.replace(" ","")
        container = container.split('/')
        for i in range(len(container)):
            float(container[i])
            
        return container

    else:
        return float(container)


#adiciona os valores ao vetor, se o valor for um vetor, utiliza extend
    #caso contrario utiliza append
for i in range(len(containers)):
    a = test_bar(containers[i].text)
    if(type(a)==type(1.0)): 
        values.append(a)
    else:
        values.extend(a)

#turn the vector into an csv file
results = pd.DataFrame(values)
results.to_csv("team_statistics.csv")  






    





