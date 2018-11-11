import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string


def is_ci_token_stopword_set_match(a, b, stopwords, threshold=0.5):
    """
        1)Pasamos todo el texto a minúscula
        2)Tomamos los signos de puntuiación
        3)Se calcula la distancia Jacquard para calcular la similitud entre ambos
    """
    tokens_a = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(a)    \
                if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(b) \
                if token.lower().strip(string.punctuation) not in stopwords]

    # Calculate Jaccard similarity
    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    return (ratio >= threshold)



def main():
    # Get default English stopwords and extend with punctuation
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(string.punctuation)
    stopwords.append('')
    is_ci_token_stopword_set_match('George Bush', 'George W. Bush',stopwords, threshold=0.5)
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()