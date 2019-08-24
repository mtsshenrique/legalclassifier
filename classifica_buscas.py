#pd = python dataanalyser
import pandas as pd

#data frame = dados que o panda colhe de arquivo
df = pd.read_csv('busca.csv')

Y_df = df['comprou']
#array como argumento com nome de mais de 1 coluna
X_df = df[['home', 'busca', 'logado']]

#transformando variavel categorica em caracteristicas binaria
Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

#transformando para vetores/arrays
X = Xdummies_df.values
Y = Ydummies_df.values



#separar 90% dos dados para treino e para teste
#codigo abaixo nunca muda
porcentagem_de_treino = 0.8
porcentagem_de_teste = 0.1

tamanho_de_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_teste = int(porcentagem_de_teste * len(Y))
tamanho_de_validacao = len(Y) - tamanho_de_treino - tamanho_de_teste


treino_dados = X[0:tamanho_de_treino]
treino_marcacoes = Y[0:tamanho_de_treino]

fim_de_treino = tamanho_de_treino + tamanho_de_teste
teste_dados = X[tamanho_de_treino:fim_de_treino]
teste_marcacoes = Y[tamanho_de_treino:fim_de_treino]


validacao_dados = X[fim_de_treino:]
validacao_marcacoes = Y[fim_de_treino:]

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes):
    modelo.fit(treino_dados, treino_marcacoes)

    resultado = modelo.predict(teste_dados)
    acertos = (resultado == teste_marcacoes)

    #soma os trues
    total_de_acertos = sum(acertos)
    total_de_elementos = len(teste_dados)
    taxa_de_acerto = 100.0 * total_de_acertos/total_de_elementos

    msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
    print (msg)
    return taxa_de_acerto




from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()

resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier",modeloAdaBoost, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)

if resultadoMultinomial > resultadoAdaBoost:
    vencedor = modeloMultinomial
else:
    vencedor = modeloAdaBoost


resultado = vencedor.predict(validacao_dados)

acertos = (resultado == teste_marcacoes)

#soma os trues
total_de_acertos = sum(acertos)
total_de_elementos = len(validacao_marcacoes)
taxa_de_acerto = 100.0 * total_de_acertos/total_de_elementos

msg = "Taxa de acerto do vencedor entre os 2 algoritmos no mundo real: {0}".format(taxa_de_acerto)
print (msg)

# a eficacia do algoritmo que chuta tudo um unico valor
from collections import Counter
acerto_base = max(Counter(validacao_marcacoes).itervalues())
taxa_de_acerto_base = 100.0 * acerto_base/len(validacao_marcacoes)
print("Taxa de acerto base: %f" % taxa_de_acerto_base)
print("Total de testes: %d" % len(validacao_dados))