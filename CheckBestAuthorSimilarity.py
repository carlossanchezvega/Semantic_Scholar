import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string

class CheckBestAuthorSimilarity:
  def __init__(self, author_a,author_b):
    self.author_a = author_a
    self.author_b = author_b
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(string.punctuation)
    stopwords.append('')
    self.stopwords = stopwords
    self.threshold=0.5



  def getSimilarity(self):
    """
    1)Pasamos  el texto a minúscula
    2)Tomamos los signos de puntuiación
    3)Se calcula la distancia Jacquard para calcular la similitud entre ambos
    """
    tokens_a = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(self.author_a)    \
                if token.lower().strip(string.punctuation) not in self.stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(self.author_b) \
                if token.lower().strip(string.punctuation) not in self.stopwords]

    # Calculate Jaccard similarity
    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    #return (ratio >= self.threshold)
    return ratio



