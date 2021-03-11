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

for doc in col.find({"Datum":{"$gt":last_update}}):
        Prüfbericht.append(doc)    
    

 
    
print(Prüfbericht)
print("hiasdf")
    


def get_device_index(article_id, device):
    for i, dev in  enumerate(device["value"]):
        #print(article_id, dev["core"]["articel_id_manufacturer"] )
        if dev["core"]["articel_id_manufacturer"] == article_id:
            # print (i)
            return i

#3) mappen der zu ändernden Attribute
def map_attributes(article_ids, instance_dynamics, inventar):     
    # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp    
    df_mapping = pd.DataFrame.from_dict(instance_dynamics)
    df_mapping.set_index("id", inplace=True)
    # print(df_mapping.head())
    df_mapping["notes"] = ""
    
    # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
    for ids in article_ids:            
        note = create_note(inventar[ids[1]])
        print(note)
        df_mapping.at[ids[2], "notes"] = note     
        # print(df_mapping.loc[ids[2]]["notes"])
    # print(df_mapping["display_name", "notes"].head())
    return df_mapping

def create_note(inventar):
    # TODO: @Robin, Zeit in lesbar convertieren
    date = str(inventar["Datum"])
    name = inventar["name"]
    defects = inventar["Mängel"]
    accept = str(inventar["accept"])    
    next_inspection = str(inventar["nächstes Prüfdatum"])
    new_note = "Pruefbericht: \n Pruefdatum: " + date + "\n Maengel: " + defects + " \n Pruefung bestanden: " + accept + "\n Naechster Prueftermin: " + next_inspection
    print (new_note)
    return new_note


#4) Put-Request der zu ändernden Artikel nach Dynamics
def update_articel(df_mapped, dynamicsApi):
    # Beispiel Upload der aktualisierten Artikel
    # result = []
    # columns = df_mapped.columns
    # for index, row in df_mapped.iterrows():
    #     # transform row zu Dataframe für json transformation
    #     df_article = pd.DataFrame([row], columns= columns)

    #     # transform to json
    #     result_json = df_article.to_json(orient="records")
    #     parsed = json.loads(result_json) [0]
    #     final_json = json.dumps(parsed, indent=4)#     

    #     # put single articles to weclapp        
    #     r = dynamicsApi.put_request(final_json, index)
    #     result.append(r)

    # json-File mit allen aktualisierten Artikeln
    result_json = df_mapped.to_json(orient="records")
    parsed = json.loads(result_json) [0]
    final_json = json.dumps(parsed, indent=4)
    print(final_json)

