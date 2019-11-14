from pandas import DataFrame
import unidecode
import os

import re

id=0
dict = {}
arqs_lidos = 0
pubs_lidas = 0
for root, dirs, files in os.walk("publicacoes"):
    for dir in dirs:
        for root, dirs_pubs, files in os.walk("publicacoes/"+dir+"/"):
            for file in files:
                file_path = "publicacoes/"+dir+"/"+file.__str__()
                #print (file_path)
                try:
                    arquivo = open(file_path,'r',encoding = "cp1252")
                    txt = arquivo.read()
                    arqs_lidos+=1
                except:
                    continue
                arquivo.close()

                #tratamento de texto
                txt = txt.lower()
                txt = unidecode.unidecode(txt)
                txt = txt.replace("\\b","").replace("\\par","").replace("\\i","")
                #divisao das publicacoes
                publicacoes = txt.split("webjur informador juridico - folha de acompanhamento processual")

                #categorias
                #1 - publicação de falência
                #2 - publicação de convolação em falencia
                #3 - publicação de extensão dos efeitos de falencia
                #4 - publicação de insolvencia civil
                #5 - publicacao de recuperacao extrajudicial
                #6 - publicação de recuperação judicial



                i=-1
                for pub in publicacoes:
                    pubs_lidas+=1
                    i+=1
                    categoria = 0

                    if re.search(r'recuperacao judicial', pub):
                        id+=1
                        print (id)
                        dict[pub] = categoria
                        continue
                    else:
                        continue

                    #if 'falencia' in pub or 'falida' in pub or 'falido' in pub:
                        #if (('decretacao de falencia' in pub or 'decretada a falencia' in pub) and 'encerramento' in pub):
                    if (('decretacao de falencia' in pub or 'decretada a falencia' in pub)):
                        categoria = 1
                        #feito
                    #if 'convolacao da recuperacao judicial em falencia' in pub and ('convolo' in pub or 'relacao de credores' in pub):
                    if 'convolacao da recuperacao judicial em falencia' in pub:
                        categoria = 2
                        #feito
                    #if 'extensao dos efeitos da falencia' in pub and 'recuperacao judicial' in pub:
                    if 'extensao dos efeitos da falencia' in pub:
                        categoria = 3
                        #feito

                    #if 'insolvencia' in pub:
                    if ('declaro a insolvencia' in pub or 'declaracao de insolvencia' in pub):
                       categoria = 4
                            #feito

                    if 'decretada a liquidacao extrajudicial' in pub:
                        categoria = 5

                    #if 'recuperacao judicial' in pub:
                        #if 'processamento da recuperacao judicial' in pub and ('concedido o processamento' in pub or 'plano de recuperacao' in pub):
                    if 'processamento da recuperacao judicial' in pub:
                       categoria = 6

                    if categoria != 0:
                        id+=0
                        dict[pub] = categoria
                        #print (id.__str__()+"\n\nPUB =>"+i.__str__()+"\nCATEGORIA IDENTIFICADA => "+categoria.__str__())
                        if (id==-300):
                            break
            if id==-300:
                break
        if id==-300:
            break
    if id==-300:
        break

print("Arquivos lidos {0}".format(arqs_lidos))
print("Pubs lidas {0}".format(pubs_lidas))
df = DataFrame(list(dict.items()), columns=['pub','categoria'])
print(df.categoria.value_counts())
export_csv = df.to_csv (r'export_dataframe_13112019.csv', index = None, header=True)