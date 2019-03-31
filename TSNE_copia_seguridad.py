from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
twenty = fetch_20newsgroups()
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot
from sklearn.metrics.pairwise import linear_kernel


from sklearn.metrics.pairwise import linear_kernel

def find_similar(tfidf_matrix, index, top_n = 5):

    # we calculare cosine similarity to know similarities between documents
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()

    # we order similarities in desc way (we do not include similarity corresponding to each sentence
    # since its similarity is equal to "1"
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]

    # we return that order
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]




def tf_idif1():
    #twenty = fetch_20newsgroups()

    twenty = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence'],
                 ['bla1', 'bla2', 'bla3']]
    list_of_sentences = []
    for sentence in twenty:
        words = ' '.join(sentence)
        list_of_sentences.append(words)
    list_of_sentences = [' '.join(sentence) for sentence in twenty]



    # fit() function in order to learn a vocabulary from one or more documents
    # transform() function on one or more documents as needed to encode each as a vector.
    #if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation
    tfidf_matrix = TfidfVectorizer().fit_transform(list_of_sentences)

    #Get the pairwise similarity matrix (n by n) (The result is the similarity matrix)
    #X = (tfidf * tfidf.T).toarray()

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(cosine_similarities)
    print('--------- MINIMO -----------\n')
    print(min([min(element) for element in cosine_similarities]))
    print('----------------------------\n')

    cosine_similarities=np.matrix(cosine_similarities)
    # We are reducing the n dimentions to 2d
    #model =TSNE(perplexity=15, n_components=2, init='pca', n_iter=3500, random_state=32)
    model =TSNE(metric="precomputed")
    distance_matrix = 1. - cosine_similarities
    Xpr = model.fit_transform(distance_matrix)


#    model =TSNE(metric="cosine")
#    Xpr = model.fit_transform(distance_matrix)

    # create a scatter plot of the projection
    pyplot.scatter(Xpr[:, 0], Xpr[:, 1])


    for i, word in enumerate(list_of_sentences):

        try:
            pyplot.annotate(word, xy=(Xpr[i, 0], Xpr[i, 1]))
        except IndexError:
            break
    pyplot.show()

    print('list_of_sentences[0] ------> list_of_sentences[0] \n')
    print('------ RANKING DE SIMILITUD ---------\n')
    for index, score in find_similar(tfidf_matrix, 1):
        print(score, list_of_sentences[index])


    # # Plot values
    # x = []
    # y = []
    # x1 = []
    # y1 = []
    #
    # for value in new_values:
    #     x.append(value[0])
    #     y.append(value[1])
    #
    # for value in new_values1:
    #     x1.append(value[0])
    #     y1.append(value[1])
    #
    # plt.figure(figsize=(10, 10))
    #
    # for i in range(len(x)):
    #     plt.scatter(x[i], y[i])
    #     plt.annotate(labels[i],
    #                  xy=(x[i], y[i]),
    #                  xytext=(5, 2),
    #                  textcoords='offset points',
    #                  ha='right',
    #                  va='bottom')
    #
    # for i in range(len(x1)):
    #     plt.scatter(x1[i], y1[i])
    #     plt.annotate(labels[i],
    #                  xy=(x1[i], y1[i]),
    #                  xytext=(5, 2),
    #                  textcoords='offset points',
    #                  ha='right',
    #                  va='bottom')
    #
    # plt.show()



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
