#encoding: utf-8

from dados import carregar_acessos

X, Y = carregar_acessos()

#minha abordagem inicial foi
#1. separar 90% para treino e 10% para teste

#primeiras 90 linhas
treino_dados = X[:90]
treino_marcacoes = Y[:90]

#ultima 9 linhas
teste_dados = X[-9:]
teste_marcacoes = Y[-9:]

from sklearn.naive_bayes import MultinomialNB
modelo = MultinomialNB()
modelo.fit(treino_dados, treino_marcacoes)


#paginas que usuario acessa ou nao => home, como_funciona, contato

print(modelo.predict([[1,0,1],[0,1,0],[1,0,0]]))

#testar para descobrir taxa de acerto

resultado = modelo.predict(teste_dados)


diferencas = resultado - teste_marcacoes
#d na frente do for é para contabiliza-lo
acertos = [ d for d in diferencas if d==0]
total_de_acertos = len(acertos)
total_de_elementos = len(teste_dados)
taxa_de_acerto = 100.0 * total_de_acertos/total_de_elementos

print(taxa_de_acerto)
print (total_de_elementos)

