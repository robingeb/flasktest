import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import requests
import xmltodict



url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"
auth = {
'username': 'HB',
'password': 'HB'
}



article_all = requests.request("GET", url, auth=(auth['username'], auth['password']))  
article_all = xmltodict.parse(article_all.text)

    #print(article_all)

    
client = pymongo.MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")
db = client['Prüfberichte']
col = db['Prüfberichte'] 

last_update = 0
Prüfbericht = []
Pruefbericht = []

for doc in col.find({"Datum":{"$gt":last_update}}):
    Prüfbericht.append(doc)    
    
Prüfbericht = str(Prüfbericht)
Prüfbericht = Prüfbericht.split(",")

for x in Prüfbericht:
    z = x.split(": ")
    Pruefbericht.append(z[1])

print(Pruefbericht)


 
Prüfdatum = Pruefbericht[5]
name = Pruefbericht[2]
maengel = Pruefbericht[1]
accept = str(Pruefbericht[3])    
next_inspection = str(Prüfbericht[4])
Prüftext = "Prüfbericht: \n Prüfdatum: " + Prüfdatum + "\n Mängel: " + maengel + " \n Prüfung bestanden: " + accept + "\n Nächster Prüftermin: " + next_inspection
print(Pruefbericht[6])

Aritkelnummer = Pruefbericht[6]

print(article_all)
