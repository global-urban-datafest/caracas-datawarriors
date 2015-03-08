import unicodedata
import re

def preprocess(corpus):
    corpus = [x.split() for x in corpus]
    corpus = [map(lambda x: (unicodedata.normalize('NFKD', x)).encode('ASCII', 'ignore'), tweet)
                  for tweet in corpus]
    corpus = [filter(lambda x: len(x)>2, tweet) for tweet in corpus]
    corpus = [filter(lambda x: x.isalnum() or re.match(r'(#|@)\w+', x), tweet) for tweet in corpus]
    corpus = [' '.join(tweet) for tweet in corpus]
    return corpus

def remove_stopwords(tweet, stopwords):
    with open(stopwords) as text:
        dictionary = text.read().split()
    tweet = tweet.split()
    tweet = filter(lambda x: x not in dictionary, tweet)
    tweet = ' '.join(tweet)
    return tweet
