import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")



db = cluster['Keys']
col = db['Updatefreq']


    
datasets = col.insert_one({"time": int(1209600)})


#zum Testen des Codes ID anpassen
#Robin: 1-10
#nico: 11-20
#Bene: 21-30
#Alpi: 31-40
post = {"_id":5, "name":"Robin", "score":1}

col.insert_one(post)