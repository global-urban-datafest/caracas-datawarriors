# -*- coding: utf-8 -*-

import pymongo
from bson.code import Code

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
            self.db.tweets.update({'id': tweet_id}, {'$set': {'sentiment': sentiment}}, upsert=True)
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_neighbourhood(self, tweet_id, neighbourhood):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'neighbourhood': neighbourhood}}, upsert=True)
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_preprocessed_text(self, tweet_id, preproc_text):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'preproc_text': preproc_text}}, upsert=True)
            return 1
        except Exception, e:
            print str(e)
            return 0

    def set_category(self, tweet_id, category):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'category': category}}, upsert=True)
            return 1
        except Exception, e:
            print str(e)
            return 0

    def get_tweet_screen_names(self):
        try:
            result = self.db.tweets.find({},{"user": 1, "id":1})
            result = [e for e in result]
            screen_names = [e["user"]["screen_name"] for e in result]
            tweet_ids = [e["id"] for e in result]
            return (tweet_ids, screen_names)
        except Exception, e:
            print str(e)
            return ([],[])

    def set_is_base_account(self, tweet_id, is_base):
        try:
            self.db.tweets.update({'id': tweet_id}, {'$set': {'is_base': is_base}})
            return 1
        except Exception, e:
            print str(e)
            return 0

    def mr_count_words(self, gov, category, collection_name):
        map = Code("function(){"
            "var text = this.preproc_text;"
            "if (text){"
            "    text = text.toLowerCase().split(/\s+/);"
            "    for (var i = text.length - 1; i >= 0; i--){"
            "    if (text[i]){"
            "            emit(text[i], 1);"
            "            }"
            "        }"
            "    }"
            "}")

        reduce = Code("function(key, values){"
            "var count = 0;"
            "values.forEach(function(v){"
                "count += v"
            "});"
            "return count;"
            "}")

        result = self.db.tweets.map_reduce(map, reduce, collection_name, query={"gov": gov, "category": category})
        return result

    def create_relevant(self, gov_id, category):
        self.db.relevants.update({'gov':gov_id, 'category':category},\
                                 {'$set': {'gov': gov_id, 'category': category}},\
                                 upsert=True)

    def set_top_relevants(self, gov_id, category, collection_name, att):
        result = self.db[collection_name].find().sort('value', -1).limit(20)
        result = [e for e in result]
        self.db.relevants.update({'gov':gov_id, 'category': category},\
                {'$set': {att: result}}, upsert=True)

    def mr_frequent_location(self, gov, category, collection_name):
        map = Code("function(){"
            "var n = this.neighbourhood;"
            "if (n){"
            "   emit(n, 1);"
            "    }"
            "}")

        reduce = Code("function(key, values){"
            "var count = 0;"
            "values.forEach(function(v){"
                "count += v"
            "});"
            "return count;"
            "}")

        result = self.db.tweets.map_reduce(map, reduce, collection_name, query={"gov": gov, "category": category})
        return result

    def drop_collection(self, collection_name):
        self.db.drop_collection(collection_name)

    def remove_documents(self, collection_name):
        self.db[collection_name].remove()
        print self.db[collection_name].count()

    def get_category_keywords(self):
        try:
            self.db.categories.find({},{"cat_id":1, "keywords":1})
            results = [e for e in results]
            keywords = [e["keywords"] for e in results]
            cat_ids = [e["cat_id"] for e in results]
            return keywords, cat_ids
        except Exception, e:
            print str(e)
            return [], []


