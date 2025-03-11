from pymongo import MongoClient, TEXT
from bson.objectid import ObjectId

connection_string = f"mongodb://{'username'}:{'password'}@{'host'}:{'port'}"
db_name = "foo"
collection_name = "bar"

mongodb : MongoClient = MongoClient(connection_string)

db = mongodb.client[db_name]
print(db.name)
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

collection = db[collection_name]
print(collection.name)

indices: list[tuple] = [
    ("key1", TEXT),
    ("key2", TEXT),
]
collection.create_index(indices)

payload = {}
res = collection.insert_one(payload)
print(res.inserted_id)

payloads = [payload]
res = collection.insert_many(payloads)
print(res.inserted_ids)

filter = {"key": "value"}
cursor = collection.find(filter)
print(cursor.to_list())

cursor = collection.find(filter={"_id": ObjectId("abcdefgh12345678abcdefgh")})
print(cursor.to_list())

query = {"$text": {"$search": "foo"}}
score = {"score": {"$meta": "textScore"}}
max_query_responses = 10

cursor = collection.find(query, score)\
    .sort([("score", {"$meta": "textScore"})])\
    .limit(max_query_responses)
print(cursor.to_list())


