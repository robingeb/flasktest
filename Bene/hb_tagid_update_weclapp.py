import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from hb_weclapp import *




# Um das letzte gespeicherte System aufzurufen:
# db = client['Keys']
# col = db['latestsystem']
# System = col.find().limit(1).sort({$natural:-1})




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
    weclapp_ids, weclapp_instances = get_articel(url,auth, tagIdeasy_ids, weClappAPI)

    # zu übertragende Werte aus TagIdeasy zu Weclapp Artikeln zuordnen und diese aktualisiert als Dataframe ausgeben
    df_mapped = map_attributes(weclapp_ids, weclapp_instances, inventar)

    # aktualisierte Artikel in Weclapp updaten (put-Request)
    update_articel(df_mapped, weClappAPI)
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
def get_articel(url, auth, ids, weClappAPI ):    
    # Abrufen aller Artikel    
    article_all = weClappAPI.get_request()
    #print(article_all)
    # Aussortieren der nicht zu updatenden Artikel
    article_update= []
    article_instances = []
    for instance in article_all["result"]:
        # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
        for i, value in enumerate(ids):
            #print(value)
            if value[0] == instance["articleNumber"]:             
                id = ids[i]                            
                # print(value[1])
                # device_index = get_device_index(value[1], device)
                # id: [Seriennummer, Artikelnummer, index in Inventar-Liste, -Index in Devicel-Liste- , Weclapp-Id] 
                # id = id + [device_index, instance["id"]]
                id.append(instance["id"])
                article_update.append(id)
                article_instances.append(instance)

            #index_inventar =  
    if len(article_update) == 0:
        #TODO. Anderen weg finden die ausführung zu stoppen(quit)
        raise Exception("Es gibt keine zu aktualisierenden Artikel") 

        
    return article_update, article_instances

def get_device_index(article_id, device):
    #print("hello")
    for i, dev in  enumerate(device["results"]):
        #print(article_id, dev["core"]["articel_id_manufacturer"] )
        if dev["core"]["articel_id_manufacturer"] == article_id:
            # print (i)
            return i

#3) mappen der zu ändernden Attribute
def map_attributes(article_ids, instance_weclapp, inventar): 
    #print(inventar[ids[1]])  

    # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp    
    df_mapping = pd.DataFrame.from_dict(instance_weclapp)
    df_mapping.set_index("id", inplace=True)
    # Version-Spalte löschen, da dieser Wert nicht geupdatet werden darf bei WeClapp (Fehlermeldung)
    df_mapping.drop('version', axis=1, inplace=True)   
    #print(df_mapping[["name", "articleNumber"]])
    # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
    for ids in article_ids: 
        
        # Beispielhaftes ändern des Namens und der Id
        # df_mapping._set_value(ids[4], "name",  device["results"][ids[3]]["core"]["device_name"]) 
        # df_mapping._set_value(ids[2], "articleNumber", ids[0] )
        custom_attributes = df_mapping.loc[ids[2]]["customAttributes"]
        #print(custom_attributes[0])
        #df_custom = pd.DataFrame.from_dict(custom_attributes)
        #df_custom._set_value(0, )
        print ("custom_attributes:")
        print(custom_attributes)
        
        try:
            update_custom_fields(inventar[ids[1]], custom_attributes[1])
        except:
            #print("Prüffelder müssen erstellt werden")
            add_custom_fields(inventar[ids[1]], custom_attributes)

        #print(custom_attributes[0]["dateValue"])
        #df_mapping._set_value(ids[2], "customAttributes")      
        
    # print(df_mapping)
    # print(df_mapping[["name", "articleNumber"]])
    return df_mapping

def update_custom_fields(inventar, custom_attributes):
    custom_attributes[0]["dateValue"] = inventar["Datum"]
    custom_attributes[1]["stringValue"] = inventar["name"]
    custom_attributes[2]["stringValue"] = inventar["Mängel"]
    custom_attributes[3]["stringValue"] = inventar["accept"]
    # custom_attributes[4]["stringValue"] = inventar[ids[1]]["Artikelnummer"]
    custom_attributes[5]["dateValue"] = inventar["nächstes Prüfdatum"]

# Prüffelder erstellen, falls noch keine vorhanden sind
# TODO: Booleand Wert anders abspeichern in MongoDB (true, false)
def add_custom_fields(inventar, custom_attributes ):    
    custom_attributes[0]["dateValue"] = inventar["Datum"]
    custom_attributes[1]["stringValue"] = inventar["name"]
    custom_attributes[2]["stringValue"] = inventar["Mängel"]
    custom_attributes[3]["stringValue"] = inventar["accept"]
    # custom_attributes[4]["stringValue"] = inventar[ids[1]]["Artikelnummer"]
    custom_attributes[5]["dateValue"] = inventar["nächstes Prüfdatum"]

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