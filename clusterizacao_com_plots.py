#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
import nltk


# In[2]:


plt.rc('font', size=16)
sns.set_style('white')


# In[3]:


df = pd.read_csv(r'export_dataframe.csv', error_bad_lines=False)


# In[4]:


from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


# In[40]:


vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
X = vectorizer.fit_transform(df['pub'][:2000])


# In[38]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=6, random_state=0)


# In[41]:


get_ipython().run_line_magic('time', 'clusters = kmeans.fit_predict(X)')


# In[49]:


from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.cm as cm

def plot_tsne_pca(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=1400, replace=False)
    
    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))
    
    
    idx = np.random.choice(range(pca.shape[0]), size=1400, replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.hsv(i/max_label) for i in label_subset[idx]]
    
    f, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')
    
    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')
    
get_ipython().run_line_magic('time', 'plot_tsne_pca(X, clusters)')


# In[50]:


def get_top_keywords(data, clusters, labels, n_terms):
    df = pd.DataFrame(data.todense()).groupby(clusters).mean()
    
    for i,r in df.iterrows():
        print('\nCluster {}'.format(i))
        print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))
            
get_top_keywords(X, clusters, vectorizer.get_feature_names(), 10)


# In[51]:


from collections import Counter
print (Counter(clusters))

