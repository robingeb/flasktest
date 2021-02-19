import pymongo
import pandas as pd


class Mongodbconnect:

    def insert_database(database, collection, datasets):
        client = pymongo.MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")
        mydb = client[database]
        mycol = mydb[collection]
        mycol.insert_many(datasets) #insert_one for 1 entry
    



#--> CSV Dateien konvertieren in JSON und automatisch in DB hochladen
# Connection DB der Unternehmen --> bestimmte ERP-Systeme

#pipenv install flask flask-pymongo python-dotenv
# init.py ln 110 = uri = ersetzen durch mongouri

client = pymongo.MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")
mydb = client["Keys"]
mycol = mydb["Key_MyFactory"]
datasets = {"R": "A"}


mycol.insert_one(datasets)