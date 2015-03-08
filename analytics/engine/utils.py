import unicodedata

def preprocess(corpus, stopwords):
    with open(stopword) as text:
        dictionary = text.read().split()
    corpus = [map(lambda x: x.split(), tweet) for tweet in corpus]
    corpus = [map(lambda x: (unicodedata.normalize('NFKD', x)).encode('ASCII', 'ignore'), tweet)
                  for tweet in corpus]
    corpus = [filter(lambda x: len(x)>2, tweet) for tweet in corpus]
    corpus = [filter(lambda x: x.isalnum() or re.match(r'(#|@)\w+', x), tweet) for tweet in corpus]
    corpus = [filter(lambda x: x not in dictionary, tweet) for tweet in corpus]
    return corpus

