import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime, date, timezone
from api.weclapp import *


def test_tagid2weclapp():
    # Authentifizierungsdaten für Weclapp-Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43' }
    mongodb_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    client = MongoClient(mongodb_url)
    updateWeClapp = UpdateWeClapp(url, auth, client) 
    print(updateWeClapp.update())

class UpdateWeClapp():
    """
    Stellt eine Udatefunktion für WeClapp zur Verfügung. 
    Prüfberichte aus dem Prüfmanagementsystem können so nach WeClapp geladen werden. 

    :param str url: gültige Zugangsurl zu Dynamics.
    :param dict auth: Authentifizierungsdaten Form: {"AuthenticationToken": string }
    :param str mongo_url: URL zur verwendeten MongoDB
    """   

    def __init__(self, url, auth, mongo):
        self.url = url
        self.auth = auth
        self.client = mongo
        self.last_update_time = 0
        self.update_time = 0
        self.update_article_number = []
        self.ids = []

    def get_update_time(self): 
        return self.update_time

    def get_article_number(self):
        return self.update_article_number


    def update(self, last_update_time = 0, actual_update_time = 0):
        """
        Führt update der Instanzen in WeClapp durch. 

        :return: gibt dict mit den aktualisierten Instanzen zurück
        """
        # reset
        self.update_article_number = []
        self.ids = []

        self.last_update_time = last_update_time

        # aktuelle update Zeit speichern
        self.update_time = actual_update_time 
        
        # Instatiate WeClapp-API
        weClappAPI = WeClappAPI(self.url, self.auth)

        # Inventar und Device Liste von TagIdeasy erhalten
        # inventar, device = get_tagideasy()
        inventar = self.get_tagideasy()

        # Liste von Ids von Instanzen im Inventar: [Artikelnummer, index in inventar-list]
        #ids = [[instance["core"]["serial_number"], instance["core"]["articel_id_buyer"], inventar["results"].index(instance) ] for instance in inventar["results"]]
        tagid_ids = [[instance["Artikelnummer"],
                          inventar.index(instance)] for instance in inventar]

        # Relevante Artikel (Geräte) aus WeClapp laden (get-Request)
        weclapp_instances = self.get_articel(
            tagid_ids, weClappAPI)
        
        if len(self.ids) == 0:
            # raise Exception("Es gibt keine zu aktualisierenden Analgen")
            return [], False

        # zu übertragende Werte aus TagIdeasy zu Weclapp Artikeln zuordnen und diese aktualisiert als Dataframe ausgeben
        df_mapped = self.map_attributes(
            weclapp_instances, inventar)

        # aktualisierte Artikel in Weclapp updaten (put-Request)
        result = self. update_articel(df_mapped, weClappAPI)
        return result, True

    # 1) Get Artikel von TagIdeasy, welche geändert werden sollen
    def get_tagideasy(self):

        # Alle Prüfberichte erhalten, welche Zeit dem letzten Update im Prüfmanagement erstellt wurden.
        data = []
        #TODO: last update auslesen und einlesen in mongodb
        # last_update = 0

        db = self.client['Prüfberichte']
        col = db['Prüfberichte']
        for doc in col.find({"Datum": {"$gt": self.last_update_time}}):
        #for doc in col.find({"Datum": {"$gt": 0}}):
            data.append(doc)
        return data
        

    # 2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
    def get_articel(self, tagid_ids, weClappAPI):
        # Abrufen aller Artikel
        try:
            article_all = weClappAPI.get_request()
        except: 
            raise Exception("Error: Zugriff auf Dynamics nicht möglich")

        # Aussortieren der nicht zu updatenden Artikel
        article_update = []
        article_instances = []
        for instance in article_all["result"]:
            # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
            for i, value in enumerate(tagid_ids):
                if value[0] == instance["articleNumber"]:
                    id = tagid_ids[i]
                    # id: [Artikelnummer, index in Inventar-Liste, -Index in Devicel-Liste- , Weclapp-Id]
                    id.append(instance["id"])
                    article_update.append(id)
                    article_instances.append(instance)
                    self.update_article_number.append(id[0])
        self.ids = article_update
        return  article_instances

    # 3) mappen der zu ändernden Attribute
    def map_attributes(self, instance_weclapp, inventar):
        # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp
        df_mapping = pd.DataFrame.from_dict(instance_weclapp)
        df_mapping.set_index("id", inplace=True)
        # Version-Spalte löschen, da dieser Wert nicht geupdatet werden darf bei WeClapp (Fehlermeldung)
        df_mapping.drop('version', axis=1, inplace=True)
        # id: [Artikelnummer, index in Inventar-Liste, -Index in Devicel-Liste- , Weclapp-Id]
        for ids in self.ids:
            custom_attributes = df_mapping.loc[ids[2]]["customAttributes"]
            try:
                self.update_custom_fields(
                    inventar[ids[1]], custom_attributes[1])
            except:
                self.add_custom_fields(inventar[ids[1]], custom_attributes)
        return df_mapping

    # Prüffelder aktualisieren
    def update_custom_fields(self, inventar, custom_attributes):
        custom_attributes[0]["dateValue"] = inventar["nächstes Prüfdatum"]
        custom_attributes[1]["stringValue"] = inventar["name"]
        custom_attributes[2]["stringValue"] = inventar["Mängel"]
        custom_attributes[3]["booleanValue"] = inventar["accept"]
        custom_attributes[5]["dateValue"] = inventar["Datum"]

    # Prüffelder erstellen, falls noch keine vorhanden sind
    def add_custom_fields(self, inventar, custom_attributes):
        custom_attributes[0]["dateValue"] = inventar["nächstes Prüfdatum"]
        custom_attributes[1]["stringValue"] = inventar["name"]
        custom_attributes[2]["stringValue"] = inventar["Mängel"]
        custom_attributes[3]["booleanValue"] = inventar["accept"]
        custom_attributes[5]["dateValue"] = inventar["Datum"]

    # 4) Put-Request der zu ändernden Artikel nach WeClapp
    def update_articel(self, df_mapped, weClappAPI):
        result = []
        columns = df_mapped.columns
        for index, row in df_mapped.iterrows():
            # transform row zu Dataframe für json transformation
            df_article = pd.DataFrame([row], columns=columns)

            # transform to json
            result_json = df_article.to_json(orient="records")
            parsed = json.loads(result_json)[0]
            final_json = json.dumps(parsed, indent=4)

            # put-request für aktualisiere Artikel
            r = weClappAPI.put_request(final_json, index)
            result.append(r)
        return result


if __name__ == "__main__":
    test_tagid2weclapp()
