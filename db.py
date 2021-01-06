import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://user1:TAMAtama12.@cluster0.hin53.mongodb.net/test")
db = cluster["Testdaten"]
collection = db["customers"]

post = {"_id":2, "name":"Robin", "score":1}

collection.insert_one(post)