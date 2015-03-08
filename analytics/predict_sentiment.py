from engine import db_interface
from engine.sentiment import feature_extractor as fe
import optparse
import pickle

parser = optparse.OptionParser()
parser.add_option('-m', '--model', help='path to serialize trained model', type='string', dest='model_out')
parser.add_option('-f', '--feat', help='path to serialize trained feature extractor', type='string', dest='feat_out')
parser.add_option('-h', '--hostname', help='hostname', type='string', dest='hostname')

(opts, args) = parser.parse_args()

mandatories = ['model_out', 'feat_out', 'hostname']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)


db = db_interface.DBInterface(opts.hostname)
db.connect()
(tweet_text, tweet_id) = db.get_tweets()
tweet_text = [x.split() for x in tweet_text]

pkl_feat = open(opts.feat_out, 'rb')
extractor = pickle.load(pkl_feat)
print "CALLING"
testset = extractor.run(tweet_text, 1)

pkl_model = open(opts.model_out, 'rb')
svm = pickle.load(pkl_model)
labels = svm.predict(testset)

inserted = 0
errors = 0

for (tid, val) in zip(tweet_id, labels):
    if db.set_predicted_sentiment(tid, val):
        inserted += 1
    else:
        errors += 1

print "inserted sentiments", inserted
print "errors inserting", errors
