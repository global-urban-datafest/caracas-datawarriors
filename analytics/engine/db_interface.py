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
