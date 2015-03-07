from pymongo import MongoClient

class DBInterface():

    def __init__(self):
        self.hostname = 'localhost'
        self.port = 27017
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.hostname, self.port)
        self.db = self.client.hackathon

    def insert_train_samples(self, documents):
        self.db.sentimentTrain.insert(documents)
