# -*- coding: utf-8 -*-

from sklearn.svm import LinearSVC
import optparse
import pickle

from engine import db_interface
from engine.sentiment import feature_extractor as fe

parser = optparse.OptionParser()
parser.add_option('-s', '--stopwords', help='stopword file', type='string', dest='stopwords')
parser.add_option('-m', '--model', help='path to serialize trained model', type='string', dest='model_out')
parser.add_option('-f', '--feat', help='path to serialize trained feature extractor', type='string', dest='feat_out')
parser.add_option('-h','--hostname', help='hostname', type='string', dest='hostname')
parser.add_option('-t', '--training size', help='size of each training batch', type='string', dest='train_size')

(opts, args) = parser.parse_args()

mandatories = ['stopwords', 'model_out', 'feat_out', 'hostname']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

db = db_interface.DBInterface(opts.hostname)
db.connect()
positives, negatives, neutral, none = db.get_training_data(opts.train_size)

examples = positives + negatives + neutral + none
labels = [1]*len(positives) + [-1]*len(negatives) + [0]*len(neutral) + [-2]*len(none)

extractor = fe.ConcatenateFeatures(
        [fe.UnigramFeatures(labels, 1000, opts.stopwords),
         fe.TweetWordCount(),
         fe.UpperWordCount(),
         fe.TitleWordCount(),
         fe.ElongatedWordCount(),
         fe.ExclamationSequenceCount(),
         fe.InterrogationSequenceCount(),
         fe.QuoteMarkCount(),
         fe.HashtagCount(),
         fe.UrlCount(),
         fe.SadEmoticonsCount(),
         fe.HappyEmoticonsCount(),
         fe.StopWordsCount(opts.stopwords)])

examples = map(lambda x: x.split(), examples)
print "Extracting features..."
trainset = extractor.run(examples)

print "Serializing feature extractor..."
output = open(opts.feat_out, 'wb')
pickle.dump(extractor, output, -1)
output.close()

print "Training..."
svm = LinearSVC(C=1.0, dual=False)
svm.fit(trainset, labels)

print "Serializing model..."

output = open(opts.model_out, 'wb')
pickle.dump(svm, output, -1)
output.close()

