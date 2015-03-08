# -*- coding: utf-8 -*-

import pymongo

class DBInterface():

    def __init__(self, hostname):
        self.hostname = hostname
        self.port = 27017
        self.client = None
        self.db = None

    def connect(self):
        self.client = pymongo.MongoClient(self.hostname, self.port)
        self.db = self.client.hackathon

    def insert_train_samples(self, documents):
        try:
            self.db.sentimentTrain.insert(documents)
            return 1
        except pymongo.errors.DuplicateKeyError:
            return 0

    def get_training_data(self, limit_size):
        try:
            res_pos = [e["text"] for e in self.db.sentimentTrain.find({'sentiment':1},{'text':1}).limit(limit_size)]
            res_neg = [e["text"] for e in self.db.sentimentTrain.find({'sentiment':-1},{'text':1}).limit(limit_size)]
            res_neu = [e["text"] for e in self.db.sentimentTrain.find({'sentiment':0},{'text':1}).limit(limit_size)]
            res_non = [e["text"] for e in self.db.sentimentTrain.find({'sentiment':-2},{'text':1}).limit(limit_size)]
            return (res_pos, res_neg, res_neu, res_non)
            print res_pos
        except Exception, e:
            print str(e)
            return ([],[],[],[])


    def set_tweet(self, tweet):
        try:
            self.db.tweets.update({'id': tweet["id"]}, {'$set': tweet}, upsert=True)
            return 1
        except Exception, e:
            print str(e)
            return 0

    def get_tweets(self):
        try:
            result = [e for e in self.db.tweets.find({},{'text':1, 'id':1})]
            print len(result)
            tweet_text = [e["text"] for e in result]
            tweet_id = [e["id"] for e in result]
            return (tweet_text, tweet_id)
        except Exception, e:
            print str(e)
            return ([], [])

    def set_predicted_sentiment(self, tweet_id, sentiment):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'sentiment': sentiment}})
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_neighbourhood(self, tweet_id, neighbourhood):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'neighbourhood': neighbourhood}})
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_preprocessed_text(self, tweet_id, preproc_text):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'preproc_text': preproc_text}})
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_category(self, tweet_id, category):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'category': category}})
            return 1
        except Exception, e:
            print str(e)
            return 0
