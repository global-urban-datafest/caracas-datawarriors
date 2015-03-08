# -*- coding: utf-8 -*-
import json
import re
import unicodedata
import optparse
from engine import utils, db_interface
from pymongo import MongoClient
from bson.code import Code


db = db_interface.DBInterface('10.250.251.16')
db.connect()


parser = optparse.OptionParser()
parser.add_option('-s', '--stopwords', help='stopword file', type='string', dest='s_filename' )
parser.add_option('-n', '--neighbourhoods', help='neighbourhood file', type='string', dest='n_filename' )
parser.add_option('-p', '--processsing', help='processing type: preproc, location, category', type='string', dest='processing' )
(opts, args) = parser.parse_args()


mandatories = ['processing']

for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

if opts.processing == 'location' and not opts.n_filename:
    print "Missing location file"
    parser.print_help()
    exit(-1)
elif (opts.processing == 'stopwords' or opts.processing == 'preproc') and not opts.s_filename:
    print "Missing stopword file"
    parser.print_help()
    exit(-1)

# preprocess
if opts.processing == 'preproc':
    prep_count = 0
    tweets, ids = db.get_tweets()
    tweets = utils.preprocess(tweets)

    for (text, id) in zip(tweets, ids):
        text = utils.remove_stopwords(text,opts.filename)
        if db.set_preprocessed_text(id, text):
            prep_count += 1
    print "Preprocessed tweets inserted:", prep_count

if opts.processing == 'location':
    loc_count = 0
    regexes = map(lambda x: "(" + x.lower() +")", )

    tweets, ids = db.get_tweets()
    tweets = utils.preprocess(tweets)

    for (text, id) in zip(tweets, ids):
        for reg in regexes:
            out = re.search(reg, text)
            if out:
                location = out.group(1)
                if db.set_neighbourhood(id, location):
                    loc_count += 1
    print "Locations inserted:", loc_count

if opts.processing == 'category':
    key_count = 0
    regexes = [r'(\W|^)(basura|aseo|reciclaje|recliclar|limpieza|desechos)(\W|$)', \
               r'(\W|^)(calle|hueco|semaforo|trafico|cola|congestion|vias|via|avenida|remolque|remolcar|ciclovia)(\W|$)', \
               r'(\W|^)(secuestro|robo|secuestraron|robaron|asaltaron|asalto|policia|inseguridad|inseguro)(\W|$)']

    categories = [0, 1, 2]

    tweets, ids = db.get_tweets()
    print len(tweets)
    tweets = utils.preprocess(tweets)

    for (text, id) in zip(tweets, ids):
        for (reg, cat) in zip(regexes, categories):
            if re.search(reg, text):
                #if cat == 0:
                #    if id== 574251050141630464:
                #        print id, text
                #    print reg, cat
                #    print text
                if db.set_category(id, cat):
                    key_count += 1

    print "Found", key_count, "in-category tweets"


