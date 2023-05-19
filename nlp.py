from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from gensim.models import Word2Vec
import numpy as np

from sentence_transformers import SentenceTransformer

import jieba
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering

def kmeans(fields):

    # Create a TfidfVectorizer object
    # vectorizer = TfidfVectorizer()

    # Use the vectorizer to transform your phrases into vectors
    # X = vectorizer.fit_transform(fields)

    # Choose the number of clusters
    num_clusters = 5

    # Create a KMeans object and use it to perform k-means clustering on your vectors
    kmeans = KMeans(n_clusters=num_clusters, random_state=33)

    # kmeans.fit(X)
    # # Print the phrases in each cluster
    # clusters = {i: [] for i in range(num_clusters)}
    # for i, label in enumerate(kmeans.labels_):
    #     clusters[label].append(fields[i])

    # Fit the KMeans model to the data
    labels = kmeans.fit_predict(bert(fields))

    # Create a dictionary with key as cluster label and value as list of sentences belonging to that cluster
    clustered_sentences = {i: [] for i in range(5)}
    for sentence, label in zip(fields, labels):
        clustered_sentences[label].append(sentence)

    # Print the sentences in each cluster
    return list(clustered_sentences.values())

def word2Vec(documents):
    # Train a Word2Vec model
    model = Word2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)

    # Function to convert a document to a vector
    def document_to_vector(document, model):
        # Convert the document to a list of vectors, then take the mean
        return np.mean([model.wv[word] for word in document], axis=0)

    # Convert all documents to vectors
    document_vectors = [document_to_vector(doc, model) for doc in documents]
    return document_vectors

def bert(documents):
    # Load the BERT model
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Assume that `texts` is your list of texts to cluster
    # texts = ["The cat says meow", "The dog says woof", ...]

    # Get a vector representation for each text
    return model.encode(documents)

def hierarchical(texts, lang):
    # segment words with jieba
    if lang == 'CN':
        texts = [" ".join(jieba.cut(text)) for text in texts]

    # vectorize texts with TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # perform hierarchical clustering
    cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
    predict_labels = cluster.fit_predict(X.toarray())

    # generate and print nested list of clusters
    clustered_texts = [[] for _ in range(5)]
    for index, label in enumerate(predict_labels):
        if lang == 'CN':
            clustered_texts[label].append(texts[index].replace(" ", ""))
        else:
            clustered_texts[label].append(texts[index])
    return clustered_texts

def spectralCluster(texts, lang):
    # segment words with jieba
    if lang == 'CN':
        texts = [" ".join(jieba.cut(text)) for text in texts]
    # vectorize texts with TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # perform spectral clustering
    clustering = SpectralClustering(n_clusters=5, assign_labels="discretize", random_state=0)
    predict_labels = clustering.fit_predict(X)

    # generate and print nested list of clusters
    clustered_texts = [[] for _ in range(5)]
    for index, label in enumerate(predict_labels):
        if lang == 'CN':
            clustered_texts[label].append(texts[index].replace(" ", ""))
        else:
            clustered_texts[label].append(texts[index])
    return clustered_texts