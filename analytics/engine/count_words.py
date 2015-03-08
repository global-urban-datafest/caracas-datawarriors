import json
from pymongo import MongoClient
from bson.code import Code

client_base = MongoClient('127.0.0.1',27017)
db = client_base.hackathon

map = Code("function(){"
    "var text = this.text;"
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



gov_id = 1
result = db.tweets.map_reduce(map, reduce, "word_count_hatillo", query={"gov": gov_id})
#db.word_count_hatillo.update({}, {category_id:}, {multi:true})

gov_id = 2
result = db.tweets.map_reduce(map, reduce, "word_count_sucre", query={"gov": gov_id})

print result
