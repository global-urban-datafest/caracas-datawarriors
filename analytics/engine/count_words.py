import json
from pymongo import MongoClient
from bson.code import Code

client_base = MongoClient('127.0.0.1',27017)
db = client_base.hackathon

map = Code("function(){"
    "var text = this.preproc_text;"
    "if (text){"
    "    text = text.toLowerCase().split(/\s+/);"
    "    print('text: ',text);"
    "    for (var i = text.length - 1; i >= 0; i--){"
    "    if (text[i]){"
    "            emit(text[i], 1);"
    "            }"
    "        }"
    "    }"
    "}")

reduce = Code("function(key, values){"
    "var count = 0;"
    "values.forEach(function(v){"
        "count += v"
    "});"
    "return count;"
    "}")

def add_attribute(texts, gov, category):
    doc = {}
    doc['words'] = []
    for e in texts:
        doc['words'].append(e)
    doc['gov'] = gov
    doc['category'] = category
    print doc

categories = [0,1,2]

for c in categories:
    print "category:", c
    collection_name = "keyword_count_h_" + str(c)
    gov_id = 1
    print collection_name
    result = db.tweets.map_reduce(map, reduce, collection_name, query={"gov": gov_id, "category": c})

    collection_name = "keyword_count_s_" + str(c)
    gov_id = 2
    print collection_name
    result = db.tweets.map_reduce(map, reduce, collection_name, query={"gov": gov_id, "category": c})




result = db.keyword_count_h_0.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 1
doc['category'] = 0
print doc
db.set_words(doc)

result = db.keyword_count_h_1.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 1
doc['category'] = 1
print doc
print
db.set_words(doc)

result = db.keyword_count_h_2.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 1
doc['category'] = 2
print doc
print
db.set_words(doc)

result = db.keyword_count_h_0.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 2
doc['category'] = 0
print doc
print
db.set_words(doc)


result = db.keyword_count_h_1.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 2
doc['category'] = 1
print doc
print
db.set_words(doc)

result = db.keyword_count_h_2.find().sort('value', -1).limit(20)
result = [e for e in result]
doc = {}
doc['words'] = []
for e in result:
    doc['words'].append(e)
doc['gov'] = 2
doc['category'] = 2
print doc
print
db.set_words(doc)


