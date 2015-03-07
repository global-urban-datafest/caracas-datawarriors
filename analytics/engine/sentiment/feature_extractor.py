# -*- coding: utf-8 -*-

import json
import re
from regex import hashtag, url, happy_emoticon, sad_emoticon
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from numpy import concatenate


class FeatureExtractor():
    def __init__(self):
        pass

    def run(self, corpus, test=False):
        pass

    def min_max(self, minim, maxim, feature):
        if maxim == 0:
            return [[0.0] for x in feature]
        return [[float(x[0]-minim)/(maxim-minim)]\
                 if x[0] < maxim else [1.0] for x in feature]

class ConcatenateFeatures(FeatureExtractor):
    def __init__(self, features=[]):
        self.features = features

    def run(self, corpus, test=False):
        concat = self.features[0].run(corpus)
        for i in range(1, len(self.features)):
            concat = concatenate((concat, \
                    self.features[i].run(corpus)), axis=1)
        return concat

class UnigramFeatures(FeatureExtractor):
    def __init__(self, stopword_file):
        with open(stopword_file) as text:
            self.dictionary = text.read().split()

    def run(self, corpus, test=False):
        corpus = [filter(lambda x: x not in self.dictionary, tweet) \
                  for tweet in corpus]
        corpus = [" ".join(tweet) for tweet in corpus]
        if not test:
            self.vectorizer = TfidfVectorizer(min_df=1)
            x_train = self.vectorizer.fit_transform(corpus)
            self.pca = PCA()
            x_train = self.pca.fit_transform(x_train.toarray())
            return x_train
        else:
            x_test = self.vectorizer.transform(corpus)
            x_test = self.pca.transform(x_test.toarray())
            return x_test

class TweetWordCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(tweet)] for tweet in corpus]
        if not test:
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class UpperWordCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: x.isupper(), tweet))]\
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class TitleWordCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: x.istitle(), tweet))]\
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class ElongatedWordCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(r'([A-Za-z])\1{3,}', x), tweet))] for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class ExclamationSequenceCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(r'(!|¡)+', x), tweet))]\
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class InterrogationSequenceCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(r'(\?|¿)+', x), tweet))] \
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class QuoteMarkCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(r'\"+', x), tweet))] \
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class HashtagCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(hashtag(), x), tweet))]\
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class UrlCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(url(), x), tweet))]\
                    for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class SadEmoticonsCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(sad_emoticon(),\
                    x), tweet))] for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class HappyEmoticonsCount(FeatureExtractor):
    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: re.search(happy_emoticon(), x), \
                    tweet))] for tweet in corpus]
        if not(test):
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)

class StopWordsCount(FeatureExtractor):
    def __init__(self, stopword_file):
        with open(stopword_file) as text:
            self.dictionary = text.read().split()

    def run(self, corpus, test=False):
        feature = [[len(filter(lambda x: x not in self.dictionary, tweet))]\
                    for tweet in corpus]
        if not test:
            self.minim = min(feature)[0]
            self.maxim = max(feature)[0]
        return self.min_max(self.minim, self.maxim, feature)


fe = ConcatenateFeatures([UnigramFeatures("spanish_stopwords.data"),
                          TweetWordCount(),
                          StopWordsCount("spanish_stopwords.data"),
                          HappyEmoticonsCount(),
                          SadEmoticonsCount(),
                          UrlCount(),
                          HashtagCount(),
                          QuoteMarkCount(),
                          InterrogationSequenceCount(),
                          ExclamationSequenceCount(),
                          ElongatedWordCount(),
                          TitleWordCount(),
                          UpperWordCount()
                          ])

#x = fe.run([["Holaaaaa", 'soy?"', "ML", ":)!"], ["YO", "#soy", "anaaaaaa", "la", "#rana!!!!"],
#["NOOO", "Soy", "una", '"rana"!!', ":(", "http://www.analarana.com"]])
#print x
