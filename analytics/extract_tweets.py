# -*- coding: utf-8 -*-

import twython
from engine import db_interface
import time
import optparse


parser = optparse.OptionParser()
parser.add_option('-f', '--file', type='string', dest='filename', action='append')
parser.add_option('-h', '--hostname', help='hostname', type='string', dest='hostname')

(opts, args) = parser.parse_args()

mandatories = ['filename', 'hostname']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)


consumer_key = "omUMc9Ix5UP8n10eNtJNfRwmj"
consumer_secret = "53mVRyd5rxsDm8x6Dqxg3gBb6FzpiiCYyXTjgNcOkoaJpgpyFo"
access_token_secret = "vPjK5qK3DNKid1wYStfX8lZEbwpEaEST3NAdqiz3FF9bp"
access_token = "83968199-rJcVfLdTCY8qvXsGNEqzIy9ZxZ3FBxEkxZzHFewg8"


api = twython.Twython(app_key=consumer_key, app_secret=consumer_secret,\
                      oauth_token=access_token, oauth_token_secret=access_token_secret)

queries = []
gov_ids = []
i = 0
for filename in opts.filename:
    queries.append(open(filename).read().split())
    queries.append(" OR ".join(query))
    queries.append(i)
    i+= 1


query = queries[0]
gov_id = [0]


db = db_interface.DBInterface(opts.hostname)
db.connect()
n_max_id = 0

inserted = 0
tweets = [1]
accum = []

extracting = True
while extracting:

    if n_max_id == 0:
        try:
            results = api.search(q=query, count=100)
        except twython.exceptions.TwythonRateLimitError:
            print "Rate limit reached, waiting for restart..."
            time.sleep(900)
            continue

        tweets = results['statuses']

        if len(tweets) == 0:
            extracting = False
            continue

        tweet_ids = [t["id"] for t in tweets]
        accum += tweet_ids
        print "tweets extracted so far", len(set(accum))

        for t in tweets:
            t["gov"] = gov_id
            if db.set_tweet(t):
                inserted += 1

        n_max_id = tweets[len(tweets)-1]['id']
        print "inserted", inserted, "tweets"


    else:
        try:
            results = api.search(q=query, count=100, max_id=n_max_id)
        except twython.exceptions.TwythonRateLimitError:
            print "Rate limit reached, waiting for restart..."
            time.sleep(900)
            continue

        tweets = results['statuses']

        if len(tweets) == 0:
            extracting = False
            continue

        tweet_ids = [t["id"] for t in tweets]
        accum += tweet_ids
        print "tweets extracted so far", len(set(accum))

        for t in tweets:
            t["gov"] = gov_id
            if db.set_tweet(t):
                inserted += 1

        n_max_id = tweets[len(tweets)-1]['id']
        print "inserted", inserted, "tweets"

