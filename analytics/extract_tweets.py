# -*- coding: utf-8 -*-

import twython
from engine import db_interface
import time

consumer_key = "omUMc9Ix5UP8n10eNtJNfRwmj"
consumer_secret = "53mVRyd5rxsDm8x6Dqxg3gBb6FzpiiCYyXTjgNcOkoaJpgpyFo"
access_token_secret = "vPjK5qK3DNKid1wYStfX8lZEbwpEaEST3NAdqiz3FF9bp"
access_token = "83968199-rJcVfLdTCY8qvXsGNEqzIy9ZxZ3FBxEkxZzHFewg8"


api = twython.Twython(app_key=consumer_key, app_secret=consumer_secret,\
                      oauth_token=access_token, oauth_token_secret=access_token_secret)

#query = "ElHatillo OR dsmolansky OR traficohatillo OR FospucaHatillo OR\
#             PoliciaHatillo OR HatilloAtiende OR SomosElHatillo"
#gov_id = 1

#query = "AlcaldiadeSucre OR CarlosOcariz OR polisucre_pms OR PCSucre \
#        OR imapsas OR obras_alc_sucre OR PorBuenCamino"
#gov_id = 2

#query = "ElHatillo OR Smolansky OR PJ_ElHatillo OR ViveElHatillo OR ADHatillo OR LaLagunita OR culturaciudadana \
#        OR ViveElHatillo OR MiAlcaldiaEnLaCalle OR CalidadDeVias OR ElHatilloBlindado OR LaBoyera OR LosPinos \
#        OR YoContribuyoPorElHatillo OR CalcoMultas OR PlanCalidadDeVias"
#gov_id = 1

query = "PadrinosPoliciales OR Imasinforma OR petare OR PorBuenCamino OR GestionaTuRollo OR PetareCamina \
         OR PoliSucre"
gov_id = 2


db = db_interface.DBInterface('192.168.1.144')
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

