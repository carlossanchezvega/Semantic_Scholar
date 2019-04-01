from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
twenty = fetch_20newsgroups()
from matplotlib import pyplot
import pylab
import os
import seaborn as sns; sns.set()
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab
from sklearn import linear_model, manifold, decomposition, datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance

colors = ['r', 'g', 'b', 'c','m','y','k']
markers = ['o', 6, '*', '^', 'h', 's']
labels = ['Documento1', 'Documento2','Documento3','Documento4','Documento5']
import numpy as np
from sklearn import datasets,manifold
from sklearn.metrics.pairwise import linear_kernel
from scipy import spatial
from sklearn.metrics import pairwise_distances



def find_similar(tfidf_matrix, index, top_n = 5):

    # we calculare cosine similarity to know similarities between documents
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()

    # we order similarities in desc way (we do not include similarity corresponding to each sentence
    # since its similarity is equal to "1"
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]

    # we return that order
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]



def plot_demo_1(distance_matrix):

    #------------------------------------------------------------------

    twenty = [['this', 'is', 'the', 'first', 'sentence', 'for', 'analysis'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['this', 'is', 'the', 'second', 'sentence'],
#              ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence'],
                 ['bla1', 'bla2', 'bla3']]
    list_of_sentences = []
    for sentence in twenty:
        words = ' '.join(sentence)
        list_of_sentences.append(words)
    documents = [' '.join(sentence) for sentence in twenty]


    #--------------------------------------------------------------------

    X= distance_matrix
    y = np.arange(len(distance_matrix))
    fig = pylab.figure(figsize=(30, 12))

    ax = fig.add_subplot(121, projection='3d')
    ax.set_facecolor('white')

    # using the precomputed dissimilarity to specify that we are passing a distance matrix:
    mds = manifold.MDS(n_components=3, dissimilarity='precomputed', random_state=1)

    # With the distance between every pair of points is preserved
    Xtrans = mds.fit_transform(X)

    for label ,color, marker in zip( np.unique(y),colors, markers):
        position=y==label
        ax.scatter(Xtrans[position,0],Xtrans[position,1], Xtrans[position,2],label="target= {0}".format(label),color=color, marker=marker, edgecolor='black')


    pylab.title("MDS on example data set in 3 dimensions")
    ax.view_init(10, -15)

    mds = manifold.MDS(n_components=2, dissimilarity='precomputed', random_state=1)
    Xtrans = mds.fit_transform(X)

    ax = fig.add_subplot(122)
    for label ,color, marker, document in zip( np.unique(y),colors, markers,documents):
        position=y==label
        ax.scatter(Xtrans[position,0],Xtrans[position,1],label=document,color=color, marker=marker, edgecolor='black')

#    ax.legend(loc="best")
    ax.legend(loc=4)

    pylab.title("MDS on example data set in 2 dimensions")

    filename = "distances.png"
    pylab.savefig(os.path.join('/home/csanchez/PycharmProjects/Semantic_Scholar', filename), bbox_inches="tight")



def tf_idif1():
    #twenty = [['documento1',['this', 'is', 'the', 'first', 'sentence', 'for', 'analysis']],
    #          ['documento2',['this', 'is', 'the', 'second', 'sentence']],
    #          ['documento3',['this', 'is', 'the', 'second', 'sentence']],
              #              ['yet', 'another', 'sentence'],
    #          ['documento4',['one', 'more', 'sentence']],
    #          ['documento5',['and', 'the', 'final', 'sentence']],
    #          ['documento6',['bla1', 'bla2', 'bla3']]]


    twenty = [['documento1',['this', 'is', 'the', 'second', 'sentence']],
              ['documento2',['this', 'is', 'the', 'second', 'sentence']],
              ['documento3',['this', 'is', 'the', 'second', 'sentence']],
              #              ['yet', 'another', 'sentence'],
              ['documento4',['this', 'is', 'the', 'second', 'sentence']],
              ['documento5',['this', 'is', 'the', 'second', 'sentence']],
              ['documento6',['this', 'is', 'the', 'second', 'sentence']]]


    corpus = []
    for file, content in twenty:
        sentence = ' '.join(content)
        corpus.append((file,sentence))

    # fit() function in order to learn a vocabulary from one or more documents
    # transform() function on one or more documents as needed to encode each as a vector.
    #if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation
    #tfidf_matrix = TfidfVectorizer().fit_transform(list_of_sentences)
    tfidf_matrix = TfidfVectorizer().fit_transform([content for file, content in corpus])
    #Get the pairwise similarity matrix (n by n) (The result is the similarity matrix)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)


    distance_matrix = pairwise_distances(tfidf_matrix, tfidf_matrix, metric='cosine', n_jobs=-1)


    #        cosine_distance = 1-pairwise_distances(tfidf_matrix, metric="cosine")

    print(cosine_similarities)


    print('--------- MINIMO -----------\n')
    print(min([min(element) for element in cosine_similarities]))
    print('----------------------------\n')

    #cosine_similarities=np.matrix(cosine_similarities)
    # We are reducing the n dimentions to 2d

    #for me_index, item in enumerate(corpus):
    #    similar_documents =  [(corpus[index], score) for index, score in find_similar(tfidf_matrix, me_index)]


    model =manifold.TSNE(metric="precomputed")

    print('--------- DISTANCE MATRIX -----------\n')
    print(distance_matrix)
    print('----------------------------\n')



    Xpr = model.fit_transform(distance_matrix)

    # create a scatter plot of the projection
    pyplot.scatter(Xpr[:, 0], Xpr[:, 1])






    for i, item in enumerate(corpus):

        try:
            pyplot.annotate(item[1], xy=(Xpr[i, 0], Xpr[i, 1]))
        except IndexError:
            break
    pyplot.show()

    print('list_of_sentences[0] ------> list_of_sentences[0] \n')
    print('------ RANKING DE SIMILITUD ---------\n')
    for index, score in find_similar(tfidf_matrix, 1):
        print(score, list_of_sentences[index])

    #plot_demo_1(cosine_similarities)
    plot_demo_1(distance_matrix)


def main():
    tf_idif1()

if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
