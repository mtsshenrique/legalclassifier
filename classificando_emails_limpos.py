#!-*- coding: utf8 -*-
texto1 = "Se eu comprar cinco anos antecipados, eu ganho algum desconto?"
texto2 = "O exercício 15 do curso de Java 1 está com a resposta errada"
texto3 = "Existe algum curso para cuidar do marketing da minha empresa?"

from collections import Counter
import pandas as pd
from sklearn.model_selection import cross_val_score
import numpy as np
import nltk


# nltk.download('punkt')

classificacoes = pd.read_csv('emails.csv', encoding='utf-8')
textos_puros = classificacoes['email']
frases = textos_puros.str.lower()
textos_quebrados = [nltk.tokenize.word_tokenize(frase) for frase in frases]


# nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

#conjunto para não permitir duplicação de elementos
dicionario = set()

#para capturar apenas a raiz das palavras
stemmer = nltk.stem.RSLPStemmer()

for lista in textos_quebrados:
    validas = [stemmer.stem(palavra) for palavra in lista if palavra not in stopwords and len(palavra)>2]
    #atualiza dicionario com todas as palavras
    dicionario.update(validas)

total_de_palavras = len(dicionario)
print (total_de_palavras)
print dicionario
#criando de x para de palavras e numeros
tuplas = zip(dicionario, xrange(total_de_palavras))

#criando dicionario => traduz palavras em indices
tradutor = {palavra:indice for palavra,indice in tuplas}


def vetorizar_texto(texto, tradutor):
    #vetorizando frase - lentradutor qtde total de palavras
    vetor = [0] * len(tradutor)

    for palavra in texto:
        if len(palavra) > 0:
            raiz = stemmer.stem(palavra)
            if raiz in tradutor:
                posicao = tradutor[raiz]
                vetor[posicao] += 1
    return vetor


#para cada texto do textos quebrados chama a funcao vetorizar texto e retorna array de todas as vetorizacoes
vetores_de_texto = [vetorizar_texto(texto, tradutor) for texto in textos_quebrados]

marcas = classificacoes['classificacao']

#classificacao

X = np.array(vetores_de_texto)
Y = np.array(marcas.tolist())

porcentagem_de_treino = 0.8
tamanho_do_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_validacao = len(Y) - tamanho_do_treino

treino_dados = X[0:tamanho_do_treino]
treino_marcacoes = Y[0:tamanho_do_treino]

validacao_dados = X[tamanho_do_treino:]
validacao_marcacoes = Y[tamanho_do_treino:]


def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes):
    k = 10
    scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv = k)
    taxa_de_acerto = np.mean(scores)
    msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
    print msg
    return taxa_de_acerto


def teste_real(modelo, validacao_dados, validacao_marcacoes):
    resultado = modelo.predict(validacao_dados)

    acertos = resultado == validacao_marcacoes

    total_de_acertos = sum(acertos)
    total_de_elementos = len(validacao_marcacoes)

    taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

    msg = "Taxa de acerto do vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_de_acerto)
    print(msg)

resultados = {}
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier(random_state=0)
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost


print (resultados)

maximo = max(resultados)
vencedor = resultados[maximo]

print ("Vencerdor: ")
print (vencedor)

vencedor.fit(treino_dados, treino_marcacoes)

teste_real(vencedor, validacao_dados, validacao_marcacoes)

acerto_base = max(Counter(validacao_marcacoes).values())
taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)
print("Taxa de acerto base: %f" % taxa_de_acerto_base)

total_de_elementos = len(validacao_dados)
print("Total de teste: %d" % total_de_elementos)
