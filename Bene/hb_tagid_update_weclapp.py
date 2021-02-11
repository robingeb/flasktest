import pandas as pd
import numpy as np
import json
from hb_weclapp import *

# Ziel ändern des Namens von "Standard-Schlinge 1A" auf "Standard-Schlinge 1AA"
# TODO: Welche Felder werden benötigt, und welche Felder sind sinnvoll zu ändern

def main():
    # information for Weclapp-Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }
    #weclapp_article_attributes =["articleNumber","name","unitId" ]

    result = []
    inventar, device = get_tagideasy()
    # Liste von Ids von Instanzen im Inventar: [Seriennummer, Artikelnummer, index in inventar-list]
    tagIdeasy_ids = [[instance["core"]["serial_number"], instance["core"]["articel_id_buyer"], inventar["results"].index(instance) ] for instance in inventar["results"]]
    

    print(tagIdeasy_ids)
    weclapp_ids, weclapp_instances = get_articel(url,auth, tagIdeasy_ids, device)
    articel_update = map_attributes(weclapp_ids, weclapp_instances, device, inventar)
    #print(weclapp_ids)


#1) Get Artikel von TagIdeasy, welche geändert werden sollen
def get_tagideasy():
    #TODO: Mit Prüfmanagementdummy verknüpfen
    with open("1_example_inventar.json") as f:
        inventar = json.loads(f.read()) 
    with open("1_example_geraete.json") as f:
        device = json.loads(f.read())
    return inventar, device

#2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
def get_articel(url, auth, ids, device ):    
    # Abrufen aller Artikel
    weClappAPI = WeClappAPI(url, auth)
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
            print (i)
            return i

#3) mappen der zu ändernden Attribute
def map_attributes(article, instance_weclapp, device, inventar):
    # Pflichtfelder von WeClapp als dict:
    mandatory_attributes = {
        "id": "3814",
        "active": True,
        "articleNumber": "012",
        "applyCashDiscount": True,
        "availableInSale": True,
        "availableInShop": False,
        "batchNumberRequired": False,
        "billOfMaterialPartDeliveryPossible": False,
        "productionArticle": False,
        "serialNumberRequired": False,
        "showOnDeliveryNote": True,
        "taxRateType": "STANDARD",
        "unitId": "2895",
        "unitName": "Stk.",
        "useAvailableForSalesChannels": False,
        "useSalesBillOfMaterialItemPrices": False,
        "useSalesBillOfMaterialItemPricesForPurchase": False,
        "name": "Fahrrad Neu"
    }

    # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp
    df_mapping = pd.DataFrame.from_dict([mandatory_attributes])
    for pos, id in range(5):   
        map_new_article = df_mapping.loc[[0],:]   
        map_new_article.index= range(df_mapping.index.max()+1,df_mapping.index.max()+len(map_new_article)+1)
        map_new_article.name =  device["results"][x]["core"]["device_name"] 
        map_new_article.unitId = x
        df_mapping = pd.concat([df_mapping,map_new_article]).sort_index()

    print(df_mapping)
    

#4) Put-Request der zu ändernden Artikel
def update_articel():
    pass

if __name__ == "__main__":
    main()