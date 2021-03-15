import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from datetime import datetime
from pymongo import MongoClient
from api.dynamics import *

def test():
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items"
    auth = {
            'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
        }
    mongodb_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    updateDynamics = UpdateDynamics(url, auth, mongodb_url)
    print(updateDynamics.update())

class UpdateDynamics():
    """
    Stellt eine Udatefunktion für Dynamics zur verfügung. Prüfberichte aus dem Prüfmanagementsystem können so nach Dynamics geladen werden. 
    Da die MyFactory API keinen POST-Requests erlaubt wird als output ein json des Prüfberichts erstellt.

    :param str url: gültige Zugangsurl zu Dynamics.
    :param dict auth: Authentifizierungsdaten Form: {"Authorization": string }
    :param str mongo_url: URL zur verwendeten MongoDB
    """   

    def __init__(self, url, auth, mongo_url):
        self.url = url
        self.auth = auth
        self.mongo_url = mongo_url

    def update(self):
        """
        Führt update der Instanzen in WeClapp durch. 

        :return: gibt json mit den (theoretisch) aktualisierten Instanzen zurück
        """
        try:
            client = MongoClient(self.mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")

        # Instantiate Dynamics-API
        dynamicsAPI = DynamicsAPI(self.url, self.auth)

        # Inventar und Device Liste von TagIdeasy erhalten
        # inventar, device = get_tagideasy()
        inventar = self.get_tagideasy(client)

        # Liste von Ids von Instanzen im Inventar: [Seriennummer, Artikelnummer, index in inventar-list]
        #tagIdeasy_ids = [[instance["core"]["serial_number"], instance["core"]["articel_id_buyer"], inventar["results"].index(instance) ] for instance in inventar["results"]]
        tagIdeasy_ids = [[instance["Artikelnummer"],
                        inventar.index(instance)] for instance in inventar]

        # Relevante Artikel (Geräte) aus Dynamics laden (get-Request)
        dynamics_ids, dynamics_instances = self.get_articel(
            self.url, self.auth, tagIdeasy_ids, dynamicsAPI)

        # zu übertragende Werte aus TagIdeasy zu Weclapp Artikeln zuordnen und diese aktualisiert als Dataframe ausgeben
        df_mapped = self.map_attributes(dynamics_ids, dynamics_instances, inventar)

        # aktualisierte Artikel in Weclapp updaten (put-Request)
        result = self.update_articel(df_mapped, dynamicsAPI)
        return result
        # print(weclapp_ids)


    # 1) Get Artikel von TagIdeasy, welche geändert werden sollen
    def get_tagideasy(self, client_mongo):

        # Collection "Prüfberichte" in MongoDB auswählen
        db = client_mongo['Prüfberichte']
        col = db['Prüfberichte']

        # Alle Prüfberichte erhalten, welche Zeit dem letzten Update von WeClapp erstellt worden sind
        # TODO: Abbruchfunktion, wenn keine Prüfberichte geladen werden konnten
        data = []
        last_update = 0
        for doc in col.find({"Datum": {"$gt": last_update}}):
            data.append(doc)
        return data
        # return daten


    # 2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
    def get_articel(self, url, auth, ids, dynamicsAPI):
        # Abrufen aller Artikel
        article_all = dynamicsAPI.get_request()

        # Aussortieren der nicht zu updatenden Artikel
        article_update = []
        article_instances = []
        for instance in article_all["value"]:
            # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
            for i, value in enumerate(ids):
                # print(value)
                if value[0] == instance["number"]:
                    id = ids[i]
                    id.append(instance["id"])
                    article_update.append(id)
                    article_instances.append(instance)
        if len(article_update) == 0:
            quit()
        return article_update, article_instances


    def get_device_index(self, article_id, device):
        # print("hello")
        for i, dev in enumerate(device["value"]):
            #print(article_id, dev["core"]["articel_id_manufacturer"] )
            if dev["core"]["articel_id_manufacturer"] == article_id:
                # print (i)
                return i

    # 3) mappen der zu ändernden Attribute
    def map_attributes(self, article_ids, instance_dynamics, inventar):
        # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp
        df_mapping = pd.DataFrame.from_dict(instance_dynamics)
        df_mapping.set_index("id", inplace=True)
        # neues Attribute ("notes") für jede Instanz erstellen, unter welcher die Prüfberichte hochgeladen werden sollen. 
        df_mapping["notes"] = ""
        # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]        
        for ids in article_ids:
            print(ids)
            note = self.create_note(inventar[ids[1]])
            df_mapping.at[ids[2], "notes"] = note
        return df_mapping


    def create_note(self, inventar):
        date = str(datetime.fromtimestamp(int(inventar["Datum"] / 1e3)))
        name = inventar["name"]
        defects = inventar["Mängel"]
        accept = str(inventar["accept"])
        next_inspection = str(inventar["nächstes Prüfdatum"])
        new_note = "Pruefbericht: \n Pruefdatum: " + date + "\n Maengel: " + defects + \
            " \n Pruefung bestanden: " + accept + \
            "\n Naechster Prueftermin: " + next_inspection
        # print(new_note)
        return new_note


    # 4) Put-Request der zu ändernden Artikel nach Dynamics
    def update_articel(self, df_mapped, dynamicsApi):
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
        parsed = json.loads(result_json)[0]
        final_json = json.dumps(parsed, indent=4)
        return final_json


if __name__ == "__main__":
    test()
