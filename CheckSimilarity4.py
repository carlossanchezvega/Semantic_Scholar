# Word2vec model for embeddings
from gensim.models import Word2Vec
# For extracting pre-trained vectors
from gensim.models import KeyedVectors
# PCA for dimensionality reduction
from sklearn.decomposition import PCA
# For ploting the results
from matplotlib import pyplot
from sklearn.manifold import TSNE

def main():
    # define training data

    keys = ['Paris', 'Python', 'Sunday', 'Tolstoy', 'Twitter']

    sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence']]

    # Defining the structure of our word2vec model

    # Size is the dimentionality feature of the model
    model_1 = Word2Vec(size=300, min_count=1)
    # Feeding Our coupus
    model_1.build_vocab(sentences)
    # Lenth of the courpus
    total_examples = model_1.corpus_count
    # traning our model

    # fit a 2d PCA model to the vectors

    # X holds the vectors of n dimentions for each word in our vocab
    X = model_1[model_1.wv.vocab]

    # We are reducing the n dimentions to 2d
    pca =TSNE(perplexity=15, n_components=2, init='pca', n_iter=3500, random_state=32)
    result = pca.fit_transform(X)

    # create a scatter plot of the projection
    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(model_1.wv.vocab)
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()


if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
