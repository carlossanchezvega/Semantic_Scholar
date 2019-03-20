from PIL.ImageOps import colorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
twenty = fetch_20newsgroups()
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
from sklearn import manifold



def tf_idif1():
    twenty = fetch_20newsgroups()

    #if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation
    tfidf = TfidfVectorizer().fit_transform(twenty.data)

    #to find the cosine distances of one document (e.g. the first in the dataset) and all of the others you just need
    # to compute the dot products of the first vector with all of the others
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()

    #scikit assumes a distance matrix for the input to TSNE
    A = np.matrix(cosine_similarities)
    A = 1. - A
    model = manifold.TSNE(metric="precomputed")
    Y = model.fit_transform(A)
    print(Y)


def plot_tsne(Y):
    # Plot values
    x = []
    y = []
    x1 = []
    y1 = []

    # for value in new_values:
    #     x.append(value[0])
    #     y.append(value[1])

    for value in Y:
        x1.append(value[0])
        y1.append(value[1])

    plt.figure(figsize=(10, 10))

    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

    for i in range(len(x1)):
        plt.scatter(x1[i], y1[i])
        plt.annotate(labels[i],
                     xy=(x1[i], y1[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

    plt.show()

def main():
    tf_idif1()








if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
