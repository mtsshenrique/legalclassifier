import csv
import os

import textract

from docx import Document

def carregar_acessos():
    #X = DADOS
    #Y = MARCACOES
    X = []
    Y = []

    arquivo = open('acesso.csv', 'rb')
    leitor = csv.reader(arquivo)

    #pula primeira linha
    leitor.next()

    #lendo as caracteristicas do csv
    for home, como_funciona, contato, comprou in leitor:
        X.append([int(home),int(como_funciona),int(contato)])
        Y.append(int(comprou))

    return X, Y

def carregar_buscas():
    #X = DADOS
    #Y = MARCACOES
    X = []
    Y = []

    arquivo = open('busca.csv', 'rb')
    leitor = csv.reader(arquivo)

    #pula primeira linha
    leitor.next()

    #lendo as caracteristicas do csv
    for home, busca, logado, comprou in leitor:
        X.append([int(home),busca,int(logado)])
        Y.append(int(comprou))

    return X, Y




def leitura_doc():
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk('publicacoes/'):
        for file in f:
            if '.doc' in file:
                files.append(os.path.join(r, file))

    for f in files:
        print(f)
        document = Document(f)
        print (document.paragraph)


leitura_doc()