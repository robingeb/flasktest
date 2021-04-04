import pandas as pd
import numpy as np
import json
from api.dynamics import *

def test_move_tagid_dynamics():
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items" 
    auth = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }
    move = MoveTagidDynamics(url, auth)
    x,y = move.export()
    print(x,y)


class MoveTagidDynamics():
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.ids = []

    def export(self):
        '''
        Exportiert Anlagen, welche nicht in Dynamics hinterlegt sind, von TagIdeasy nach Dynamics

        :return ids: Artikel-Nummern der exportierten Anlagen
        :return result: json-Form der exportierten Anlagen
        '''

        # reset
        self.ids = []

        # Minimum der benötigten Attribute von Dynamics für einen erfolgreichen POST-Request
        dynamics_article_attributes = ["number", "displayName"]

        result = []

        # Geräte Instanzen aus TagIdeasy erhalten
        x, y = self.get_tagideasy()

        # Geräte zum API Input-Schema von Dynamics mappen
        devices_mapped = self.map_attributes(x, y, dynamics_article_attributes)

        # initialice WeClappAPI
        dynamicsAPI = DynamicsAPI(self.url, self.auth)

        # Durch Anlagen Iterieren und nach Dynamics pushen
        for index, row in devices_mapped.iterrows():
            df_article = pd.DataFrame([row], columns=dynamics_article_attributes)
            # transform to json
            result_json = df_article.to_json(orient="records")
            parsed = json.loads(result_json)[0]
            final_json = json.dumps(parsed, indent=4)
            
            # push single articles to weclapp
            r = dynamicsAPI.post_request(final_json)
            if "error" not in r:
                self.ids.append(row["number"])

            result.append(r)
        
        return self.ids, result


    def get_tagideasy(self):
        with open("tagideasy_json/1_example_inventar.json") as f:
            inventar = json.loads(f.read())
        with open("tagideasy_json/1_example_geraete.json") as f:
            device = json.loads(f.read())
        return inventar, device


    def map_attributes(self, inventar, device, weclapp_article_attributes):

        # get serial number from v1_inventar and match as articel number
        article_number = [inventar["results"][x]["core"]["inventory_number"]
                        for x in range(len(inventar["results"]))]

        # get article id to identify the device-categorie in geräte_v1
        article_id = [inventar["results"][x]["core"]["articel_id_buyer"]
                    for x in range(len(inventar["results"]))]

        # get device name from geräte_v1 with help of the article id
        device_name = []
        for x in range(len(inventar["results"])):
            for y in range(len(device["results"])):
                if device["results"][y]["core"]["articel_id_manufacturer"] == article_id[x]:
                    device_name.append(device["results"][y]["core"]["device_name"])

        articles = np.array([article_number, device_name])
        articles = articles.transpose()
        df_articles = pd.DataFrame(articles, columns=weclapp_article_attributes)
        return df_articles


if __name__ == "__main__":
    test_move_tagid_dynamics()
