import optparse
import re
import tweepy
import time
import json

class TrainsetConstructor():

    def __init__(self, filename, db):
        self.filename = filename
        self.api = None
        self.auth = None
        self.access_token_secret="vPjK5qK3DNKid1wYStfX8lZEbwpEaEST3NAdqiz3FF9bp"
        self.access_token="83968199-rJcVfLdTCY8qvXsGNEqzIy9ZxZ3FBxEkxZzHFewg8"
        self.c_key = "omUMc9Ix5UP8n10eNtJNfRwmj"
        self.c_secret = "53mVRyd5rxsDm8x6Dqxg3gBb6FzpiiCYyXTjgNcOkoaJpgpyFo"
        self.db = db

    def authenticate(self):
        self.auth = tweepy.OAuthHandler(consumer_key=self.c_key, consumer_secret=self.c_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)

    def parse_file(self):
        def normalize_value(x):
            if x == "P" or x == "P+":
                return 1
            elif x == "N" or x == "N+":
                return -1
            elif x == "NEU":
                return 0

        text = open(self.filename).read()
        tweet_id = re.findall('<tweetid>(\d+)</tweetid>', text)
        value = re.findall('<polarity>\n*<value>(\w+\+*)</value>', text)
        print "parsed ids", len(tweet_id)
        print "parsed values", len(value)
        if len(tweet_id) != len(value):
            print "ids and values do not correspond, check parsing method"
            exit(-1)
        tweet_id, value = zip(*filter(lambda (_,val): val != "NONE", zip(tweet_id, value)))
        value = map(lambda x: normalize_value(x), value)
        tweet_id = map(lambda x: int(x), tweet_id)
        return tweet_id, value

    def run(self):
        self.authenticate()
        tweet_id, sentiment = self.parse_file()

        running = 1
        index = 0

        self.db.connect()

        while running:

            if index > len(tweet_id):
                running = False
                continue

            batch_tweet_id = tweet_id[index:index+100]
            batch_sentiment = sentiment[index:index+100]

            try:
                tweets = self.api.statuses_lookup(batch_tweet_id)
                ## add sentiment to tweet object
                documents = []
                for (stat, val) in zip(tweets, sentiment):
                    doc = stat._json
                    doc['sentiment'] = val
                    documents.append(doc)

                self.db.insert_train_samples(documents)

                index += 100
                print "tweets inserted", index

            except tweepy.TweepError as e:
                if e[0][u'code'] == 88:
                    print e[0][u'message']
                    print "wating 15 mins to restart"
                    time.sleep(900)
                else:
                    print e[0][u'message']
                    print "index", index
                    time.sleep(1)



