import gensim



def tf_idif1():

    model_gn = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)



def load_data(FileName = './EN-wform.w.5.cbow.neg10.400.subsmpl.txt'):

    embeddings = {}
    file = open(FileName,'r')
    i = 0
    print ("Loading word embeddings first time")
    for line in file:
        # print line

        tokens = line.split('\t')

        #since each line's last token content '\n'
        # we need to remove that
        tokens[-1] = tokens[-1].strip()

        #each line has 400 tokens
        for i in xrange(1, len(tokens)):
            tokens[i] = float(tokens[i])

        embeddings[tokens[0]] = tokens[1:-1]
    print "finished"
    return embeddings

e = load_data()




def main():
    sentence1 = "Four people died in an accident."

    sentence2 = "4 men are dead from a collision"







if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
