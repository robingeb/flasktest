import pandas as pd
import numpy as np
import json
from api.weclapp import *

def test_move_weclapp_tagid():
    # information for Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
        'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }
    move = MoveWeclappTagid(url, auth)
    move.export([10000,20000])
    print(move.get_article_number())

class MoveWeclappTagid():
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.export_article_number = []

    def get_article_number(self):
        return self.export_article_number

    
    def export(self, article_number_range = [0,0]):
        '''
        Exportiert Anlagen von Weclapp nach TagIdeasy

        :param article_number_range: Wertebereich der Artikel-Nummer zum Einschränken des Exports auf Anlagen. 
        Wenn [0,0] wird dieser nicht eingschränkt.

        :return ids: Artikel-Nummern der exportierten Anlagen
        :return result: json-Form der exportierten Anlagen
        '''
        # reset
        self.export_article_number = []
        
        # initialice WeClappAPI und Geräte-Instanzen als Liste ausgeben
        weClappAPI = WeClappAPI(self.url, self.auth)
        machine_instances = self.get_weclapp(weClappAPI, article_number_range)

        # Datenstruktur von TagIdeasy 
        device, inventar = self.get_tagideasy()


        # Geräte zum API Input-Schema von TagIdeasy mappen
        mapped_inventar, mapped_device = self.map_attributes(device, inventar, machine_instances)

        # Ausgeben der beiden Listen. Kein Upload da TagIdeasy nicht gegeben.
        df_inventar = pd.DataFrame.from_dict(mapped_inventar)
        df_device = pd.DataFrame.from_dict(mapped_device)

        # transform zu json für API Upload (nicht umsetzbar)
        result_json = df_inventar.to_json(orient="records")
        parsed = json.loads(result_json)
        inventar_json = json.dumps(parsed, indent=4)

        result_json = df_device.to_json(orient="records")
        parsed = json.loads(result_json)
        device_json = json.dumps(parsed, indent=4)

        # print(inventar_json)
        # print(device_json)
        return self.export_article_number, [mapped_inventar, mapped_device]


    def get_tagideasy(self):
        with open("tagideasy_json/Datenstruktur_Geräte.json") as f:
            inventar = json.loads(f.read())
        with open("tagideasy_json/Datenstruktur_Inventar.json") as f:
            device = json.loads(f.read())
        return inventar, device

    def get_weclapp(self, weClappAPI, article_number_range):
            # Abrufen aller Artikel
            article_all = weClappAPI.get_request()

            # Articel-number
            min_article_number = int(article_number_range[0])
            max_article_number = int(article_number_range[1])

            # Aussortieren der nicht zu updatenden Artikel
            machine_instances = []
            for instance in article_all["result"]:
                an = int(instance["articleNumber"])
                # Wenn Range [0,0], dann Suche nicht eingrenzen.
                if article_number_range != [0,0]: 
                    # Suche nur auf Anlagen eingrenzen 
                    if an >= min_article_number and an < max_article_number:
                        machine_instances.append(instance)
                else:
                    machine_instances.append(instance)
            return  machine_instances


    def map_attributes(self, inventar, device, machine_instances):

        # Erstellen zweier Listen gemäß der Datenstruktur von TagIdeasy
        instances_inventar = []
        instances_device = []

        #for x in range(len(machine_instances)): 
        for instance in machine_instances:           
            inventar_add = inventar
            device_add = device
            article_number = instance["articleNumber"]
            inventar_add["core"]["inventory_number"] = article_number
            device_add["core"]["device_name"] = instance["name"]
            instances_inventar.append(inventar_add)
            instances_device.append(device_add)
            self.export_article_number.append(article_number)
        
        return instances_inventar, instances_device



if __name__ == "__main__":
    test_move_weclapp_tagid()
