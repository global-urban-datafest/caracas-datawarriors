import pymongo

class DBInterface():

    def __init__(self):
        self.hostname = 'localhost'
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
        print "get_training_data"
        print self.db
        try:
            res_pos = self.db.sentimentTrain.find({'sentiment':1},{'text':1}).limit(limit_size)
            res_neg = self.db.sentimentTrain.find({'sentiment':-1},{'text':1}).limit(limit_size)
            res_neu = self.db.sentimentTrain.find({'sentiment':0},{'text':1}).limit(limit_size)
            res_non = self.db.sentimentTrain.find({'sentiment':-2},{'text':1}).limit(limit_size)
            print res_pos
            print len(res_pos), len(res_neg), len(res_neu), len(res_none)
            return (res_pos, res_neg, res_neu, res_non)
        except Exception, e:
            print str(e)

