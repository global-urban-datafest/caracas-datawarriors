import twython
from engine import db_interface

consumer_key = "omUMc9Ix5UP8n10eNtJNfRwmj"
consumer_secret = "53mVRyd5rxsDm8x6Dqxg3gBb6FzpiiCYyXTjgNcOkoaJpgpyFo"
access_token_secret = "vPjK5qK3DNKid1wYStfX8lZEbwpEaEST3NAdqiz3FF9bp"
access_token = "83968199-rJcVfLdTCY8qvXsGNEqzIy9ZxZ3FBxEkxZzHFewg8"





api = twython.Twython(app_key=consumer_key, app_secret=consumer_secret,\
                      oauth_token=access_token, oauth_token_secret=access_token_secret)

#query = "ElHatillo OR dsmolansky OR traficohatillo OR FospucaHatillo OR\
#             PoliciaHatillo OR HatilloAtiende OR SomosElHatillo"
query = "AlcaldiadeSucre OR CarlosOcariz OR polisucre_pms OR PCSucre \
        OR imapsas OR obras_alc_sucre OR PorBuenCamino"

db = db_interface.DBInterface('192.168.1.144')
db.connect()
n_max_id = 0

inserted = 0
tweets = [1]
accum = []

#for gov in governments:
while 1:

    #if len(tweets) == 0:
    #    continue


    if n_max_id == 0:
        results = api.search(q=query, count=100)
        tweets = results['statuses']
        tweet_ids = [t["id"] for t in tweets]
        accum += tweet_ids
        print "tweets extracted so far", len(set(accum))

        for t in tweets:
            t["gov"] = 1
            if db.set_tweet(t):
                inserted += 1

        n_max_id = tweets[len(tweets)-1]['id']
        print "inserted", inserted, "tweets"


    else:
        results = api.search(q=query, count=100, max_id=n_max_id)
        tweets = results['statuses']
        tweet_ids = [t["id"] for t in tweets]

        accum += tweet_ids
        print "tweets extracted so far", len(set(accum))

        for t in tweets:
            t["gov"] = 2
            if db.set_tweet(t):
                inserted += 1

        n_max_id = tweets[len(tweets)-1]['id']
        print "inserted", inserted, "tweets"


