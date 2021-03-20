import pandas as pd
import numpy as np
import json
from api.weclapp import *

#   Items müssen vor Testem aus Weclapp wieder gelöscht werden, damit der Import funktioniert
def main():

    # information for Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
        'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }

    # initialice WeClappAPI und Geräte erhalten
    weClappAPI = WeClappAPI(url, auth)
    machine_instances = get_weclapp(weClappAPI)

    # Minimum der benötigten Attribute von WeClapp für einen erfolgreichen POST-Request
    # weclapp_article_attributes = ["articleNumber", "name", "unitId"]

    # Datenstruktur von TagIdeasy 
    device, inventar = get_tagideasy()



    result = []

    # Geräte Instanzen aus WeClapp erhalten
    # x, y = get_tagweclapp()

    # Geräte zum API Input-Schema von WeClapp mappen
    mapped_inventar, mapped_device = map_attributes(device, inventar, machine_instances)

    

    # TODO: Existiert möglichkeit mehrere Artikel auf einmal zu pushen?

    # Iterate throug articles and push them to weclapp
    # for index, row in devices_mapped.iterrows():
    #     df_article = pd.DataFrame([row], columns=weclapp_article_attributes)
    #     # transform to json
    #     result_json = df_article.to_json(orient="records")
    #     parsed = json.loads(result_json)[0]
    #     final_json = json.dumps(parsed, indent=4)
    #     print(final_json)
    #     # push single articles to weclapp
    #     r = weClappAPI.post_request(final_json)
    #     result.append(r)
    print(mapped_inventar)
    print(mapped_device)
    return result


def get_tagideasy():
    with open("tagideasy_json/Datenstruktur_Geräte.json") as f:
        inventar = json.loads(f.read())
    with open("tagideasy_json/Datenstruktur_Inventar.json") as f:
        device = json.loads(f.read())
    return inventar, device

def get_weclapp(weClappAPI):
        # Abrufen aller Artikel
        article_all = weClappAPI.get_request()

        # Aussortieren der nicht zu updatenden Artikel
        machine_instances = []
        for instance in article_all["result"]:
            # Suche nur auf Anlagen eingrenzen (hier Beispielhaft: ArtikelNummer >100 für Anlagen)
            if int(instance["articleNumber"]) >= 1000 & int(instance["articleNumber"]) <2000:
                machine_instances.append(instance)
        return  machine_instances


def map_attributes(inventar, device, machine_instances):

    instances_inventar = []
    instances_device = []
    for x in range(len(machine_instances)):
        print(x)
        inventar_add = inventar
        device_add = device
        inventar_add["core"]["inventory_number"] = machine_instances[x]["articleNumber"]
        device_add["core"]["device_name"] = machine_instances[x]["name"]
        instances_inventar.append(inventar_add)
        instances_device.append(device_add)
    
    return instances_inventar, instances_device


    # # get serial number from v1_inventar and match as articel number
    # article_number = [inventar["results"][x]["core"]["inventory_number"]
    #                   for x in range(len(inventar["results"]))]

    # # get article id to identify the device-categorie in geräte_v1
    # article_id = [inventar["results"][x]["core"]["articel_id_buyer"]
    #               for x in range(len(inventar["results"]))]

    # # get device name from geräte_v1 with help of the article id
    # device_name = []
    # for x in range(len(inventar["results"])):
    #     for y in range(len(device["results"])):
    #         if device["results"][y]["core"]["articel_id_manufacturer"] == article_id[x]:
    #             device_name.append(device["results"][y]["core"]["device_name"])

    # # generate unit_id (2895 for Stk. )
    # id = 2895
    # unit_id = [id] * len(article_id)

    # articles = np.array([article_number, device_name, unit_id])
    # articles = articles.transpose()
    # df_articles = pd.DataFrame(articles, columns=weclapp_article_attributes)
    # #result_json = df_articles.to_json(orient="records")
    return df_articles


if __name__ == "__main__":
    main()
