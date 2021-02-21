import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from hb_weclapp import *

# Ziel ändern des Namens von "Standard-Schlinge 1A" auf "Standard-Schlinge 1AA"
# TODO: Welche Felder werden benötigt, und welche Felder sind sinnvoll zu ändern

def main():
    # Authentifizierungsdaten für Weclapp-Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }

    # MongoDB
    # app.config["MONGO_URI"] = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    # mongo = PyMongo(app)
    client = MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")
    
    #Instatiate WeClapp-API
    weClappAPI = WeClappAPI(url, auth)
    
    # Inventar und Device Liste von TagIdeasy erhalten
    # inventar, device = get_tagideasy()
    inventar = get_tagideasy(client)

    # Liste von Ids von Instanzen im Inventar: [Seriennummer, Artikelnummer, index in inventar-list]
    #tagIdeasy_ids = [[instance["core"]["serial_number"], instance["core"]["articel_id_buyer"], inventar["results"].index(instance) ] for instance in inventar["results"]]
    tagIdeasy_ids = [[instance["Artikelnummer"], inventar.index(instance)] for instance in inventar]
    print(tagIdeasy_ids)

    # Relevante Artikel (Geräte) aus WeClapp laden (get-Request)
    #weclapp_ids, weclapp_instances = get_articel(url,auth, tagIdeasy_ids, device, weClappAPI)

    # zu übertragende Werte aus TagIdeasy zu Weclapp Artikeln zuordnen und diese aktualisiert als Dataframe ausgeben
    #df_mapped = map_attributes(weclapp_ids, weclapp_instances, device, inventar)

    # aktualisierte Artikel in Weclapp updaten (put-Request)
    #update_articel(df_mapped, weClappAPI)
    #print(weclapp_ids)


#1) Get Artikel von TagIdeasy, welche geändert werden sollen
def get_tagideasy(client_mongo):
    #TODO: Mit Prüfmanagementdummy verknüpfen
    # with open("1_example_inventar.json") as f:
    #     inventar = json.loads(f.read()) 
    # with open("1_example_geraete.json") as f:
    #     device = json.loads(f.read())
    # return inventar, device

    # Collection "Prüfberichte" in MongoDB auswählen
    db = client_mongo['Prüfberichte']
    col = db['Prüfberichte']
    #daten = col.find_one({"Artikelnummer": "002"})

    # Alle Prüfberichte erhalten, welche Zeit dem letzten Update von WeClapp erstellt worden sind
    # TODO: Abbruchfunktion, wenn keine Prüfberichte geladen werden konnten
    data = []
    last_update = 0
    for doc in col.find({"Datum":{"$gt":last_update}}):
        data.append(doc)    
    return data
    #return daten
    

#2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
def get_articel(url, auth, ids, device, weClappAPI ):    
    # Abrufen aller Artikel    
    article_all = weClappAPI.get_request()
    #print(article_all)
    # Aussortieren der nicht zu updatenden Artikel
    article_update= []
    article_instances = []
    for instance in article_all["result"]:
        for i, value in enumerate(ids):
            #print(value)
            if value[0] == instance["articleNumber"]:             
                id = ids[i]                            
                print(value[1])
                device_index = get_device_index(value[1], device)
                # id: [Seriennummer, Artikelnummer, index in Inventar-Liste, Index in Devicel-Liste , Weclapp-Id] 
                id = id + [device_index, instance["id"]]
                article_update.append(id)
                article_instances.append(instance)

            #index_inventar =  
    print(article_update)
    #TODO: Testen, ob alle Devices von TagIdesay in Weclapp bereits angelegt sind, wenn nicht fehlende Werde ausgeben    
    return article_update, article_instances

def get_device_index(article_id, device):
    #print("hello")
    for i, dev in  enumerate(device["results"]):
        #print(article_id, dev["core"]["articel_id_manufacturer"] )
        if dev["core"]["articel_id_manufacturer"] == article_id:
            # print (i)
            return i

#3) mappen der zu ändernden Attribute
def map_attributes(article_ids, instance_weclapp, device, inventar):   

    # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp    
    df_mapping = pd.DataFrame.from_dict(instance_weclapp)
    df_mapping.set_index("id", inplace=True)
    # Version-Spalte löschen, da dieser Wert nicht geupdatet werden darf bei WeClapp (Fehlermeldung)
    df_mapping.drop('version', axis=1, inplace=True)   
    print(df_mapping[["name", "articleNumber"]])
    for ids in article_ids: 
        # Beispielhaftes ändern des Namens und der Id
        df_mapping._set_value(ids[4], "name",  device["results"][ids[3]]["core"]["device_name"]) 
        df_mapping._set_value(ids[4], "articleNumber", ids[0] )
       
        
    # print(df_mapping)
    print(df_mapping[["name", "articleNumber"]])
    return df_mapping

#4) Put-Request der zu ändernden Artikel nach WeClapp
def update_articel(df_mapped, weClappAPI):
    result = []
    columns = df_mapped.columns
    for index, row in df_mapped.iterrows():
        # transform row zu Dataframe für json transformation
        df_article = pd.DataFrame([row], columns= columns)
        #df_article = df_article.rename_axis('id').reset_index()
        # print(df_article)

        # transform to json
        result_json = df_article.to_json(orient="records")
        parsed = json.loads(result_json) [0]
        final_json = json.dumps(parsed, indent=4)
        # print(final_json)

        # put single articles to weclapp        
        r = weClappAPI.put_request(final_json, index)
        result.append(r)
    print(result)

if __name__ == "__main__":
    main()