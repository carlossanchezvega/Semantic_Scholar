import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string


def is_ci_token_stopword_set_match(a, b, threshold=0.5):
    """Check if a and b are matches."""
    tokens_a = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(a) \
                if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(b) \
                if token.lower().strip(string.punctuation) not in stopwords]

    # Calculate Jaccard similarity
    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    return (ratio >= threshold)



def main():
    # Get default English stopwords and extend with punctuation
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(string.punctuation)
    stopwords.append('')

    # Create tokenizer and stemmer
    tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()

    is_ci_token_stopword_set_match('George Bush', 'George W. Bush', threshold=0.5)
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()