from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import stopwords

import csv
import sys



def clusterizacao():
    import numpy  as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from nltk.corpus import stopwords

    # set font size of labels on matplotlib plots
    plt.rc('font', size=16)

    # set style of plots
    sns.set_style('white')

    df = pd.read_csv('export_dataframe.csv')

    #capturando frequencias de palavras dos textos

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
    X = vectorizer.fit_transform(df['pub'][:100])


    #dados
    #X = np.array(pubs)
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=6, random_state=0)
    kmeans.fit(X)
    y = kmeans.labels_
    df['labels_cluster'] = pd.Series(kmeans.labels_)


    #sns.lmplot(data=df,x=5,y=5, hue='labels_cluster',fit_reg=False, legend=True, legend_out=True)

    sns.pairplot(df[:100],hue='labels_cluster', vars=df['labels_cluster'])
    print ("Done")

clusterizacao()

csv.field_size_limit(sys.maxsize)
publicacoes = []
arquivo = open('export_dataframe.csv', 'r')
leitor = csv.reader(arquivo)

for pub in leitor:
    publicacoes.append(pub[0])

print(len(publicacoes))

vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(publicacoes)

true_k = 6
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])


print("\n")
print("Prediction")

Y = vectorizer.transform(["chrome browser to open."])
prediction = model.predict(Y)
print(prediction)

Y = vectorizer.transform(["My cat is hungry."])
prediction = model.predict(Y)
print(prediction)