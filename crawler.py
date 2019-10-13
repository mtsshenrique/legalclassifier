from datetime import datetime
from datetime import timedelta

import time
import os

import requests
from bs4 import BeautifulSoup

print (datetime.now().date())


#ultimo dia executado - 2018-06-26

#laço para percorrer do dia x até data de hoje
#somar dia
data_atual = datetime.now().date() - timedelta(days=2)
data_inicial_webjur = (datetime.strptime('May 24 2018', '%b %d %Y')).date()
data_webjur = data_inicial_webjur
print (data_inicial_webjur)

while(data_webjur <= data_atual):
    data_webjur = data_webjur + timedelta(days=1)
    print("\n\n\n\n")
    print("*"*30)
    print("DOWNLOAD PUBLICACOES DE "+data_webjur.__str__())
    time.sleep(3)
    url = "http://webjur.com.br/bb/EDITAIS/"+data_webjur.__str__().replace("-","")+"/"
    response = requests.get(url=url)
    raw_page_html = BeautifulSoup(response.text, 'html.parser')
    links = raw_page_html.find_all('a')
    for link in links:
        href = link['href']
        if 'doc' in href:
            r = requests.get(url="http://webjur.com.br"+href)
            time.sleep(1)
            if r.text=='':
                print("ARQ VAZIO")
                continue
            #cria pasta pro mes
            path = 'publicacoes/'+data_webjur.year.__str__()+data_webjur.month.__str__()+"/"
            if not os.path.exists(path):
                os.mkdir(path)
            #captura nome do arquivo do att href
            split = href.split("/")
            name_file = split[len(split)-1]
            #salva arquivo do response em diretorio
            f = open(path+name_file, 'wb')
            f.write(r.content)
            f.close()
            print ("ARQ BAIXADO "+name_file)

