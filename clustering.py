from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import os

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=200000)
#loading
fileList = os.listdir('seg')
corpora = []
for filename in fileList:
    with open('seg/' + filename, 'r') as f:
        corpora.append(f.read().strip())

tfidf_matrix = tfidf_vectorizer.fit_transform(corpora)
#print(tfidf_matrix.shape)
#print(tfidf_vectorizer.get_feature_names())
#dist = 1 - cosine_similarity(tfidf_matrix)
#print(dist)

num_clusters = 3

km = KMeans(n_clusters=num_clusters, n_init=50)
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()
print(clusters)
