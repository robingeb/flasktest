import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from api.weclapp import *


# def test():
#     # Authentifizierungsdaten für Weclapp-Request
#     url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
#     auth = {'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43' }
#     mongodb_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
#     updateWeClapp = UpdateWeClapp(url, auth, mongodb_url)
#     updateWeClapp.update()

class UpdateWeClapp():
    def __init__(self, url, auth, mongo_url):
        self.url = url
        self.auth = auth
        self.mongo_url = mongo_url

    def update(self):
        # MongoDB instantiate
        # TODO: PF. connection failed (wie darauf reagieren, Ausgabe: Error, Datenbank Zugriff nicht möglich)
        try:
            client = MongoClient(self.mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")

        # Instatiate WeClapp-API
        weClappAPI = WeClappAPI(self.url, self.auth)

        # Inventar und Device Liste von TagIdeasy erhalten
        # inventar, device = get_tagideasy()
        inventar = self.get_tagideasy(client)

        # Liste von Ids von Instanzen im Inventar: [Seriennummer, Artikelnummer, index in inventar-list]
        #tagIdeasy_ids = [[instance["core"]["serial_number"], instance["core"]["articel_id_buyer"], inventar["results"].index(instance) ] for instance in inventar["results"]]
        tagIdeasy_ids = [[instance["Artikelnummer"],
                          inventar.index(instance)] for instance in inventar]

        # Relevante Artikel (Geräte) aus WeClapp laden (get-Request)
        weclapp_ids, weclapp_instances = self.get_articel(
            tagIdeasy_ids, weClappAPI)

        # zu übertragende Werte aus TagIdeasy zu Weclapp Artikeln zuordnen und diese aktualisiert als Dataframe ausgeben
        df_mapped = self.map_attributes(
            weclapp_ids, weclapp_instances, inventar)

        # aktualisierte Artikel in Weclapp updaten (put-Request)
        result = self. update_articel(df_mapped, weClappAPI)
        return result

    # 1) Get Artikel von TagIdeasy, welche geändert werden sollen
    def get_tagideasy(self, client_mongo):

        # Collection "Prüfberichte" in MongoDB auswählen
        db = client_mongo['Prüfberichte']
        col = db['Prüfberichte']
        #daten = col.find_one({"Artikelnummer": "002"})

        # Alle Prüfberichte erhalten, welche Zeit dem letzten Update von WeClapp erstellt worden sind
        # TODO: Abbruchfunktion, wenn keine Prüfberichte geladen werden konnten
        # TODO: Falsche Url, Authentifizierung
        data = []
        last_update = 0
        for doc in col.find({"Datum": {"$gt": last_update}}):
            data.append(doc)
        return data
        # return daten

    # 2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
    def get_articel(self, ids, weClappAPI):
        # Abrufen aller Artikel
        try:
            article_all = weClappAPI.get_request()
        except:
            raise Exception(
                "Connection Failed \n Überprüfe: \n fehlerhafte URL oder Authentifizerungsdaten")
        # print(article_all)

        # Aussortieren der nicht zu updatenden Artikel
        article_update = []
        article_instances = []
        for instance in article_all["result"]:
            # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
            for i, value in enumerate(ids):
                if value[0] == instance["articleNumber"]:
                    id = ids[i]
                    # id: [Seriennummer, Artikelnummer, index in Inventar-Liste, -Index in Devicel-Liste- , Weclapp-Id]
                    id.append(instance["id"])
                    article_update.append(id)
                    article_instances.append(instance)

                # index_inventar =
        if len(article_update) == 0:
            # TODO. quti testen mit JobScheduler
            # raise Exception("Es gibt keine zu aktualisierenden Artikel")
            quit()

        return article_update, article_instances

    # def get_device_index(self, article_id, device):
    #     #print("hello")
    #     for i, dev in  enumerate(device["results"]):
    #         #print(article_id, dev["core"]["articel_id_manufacturer"] )
    #         if dev["core"]["articel_id_manufacturer"] == article_id:
    #             # print (i)
    #             return i

    # 3) mappen der zu ändernden Attribute
    def map_attributes(self, article_ids, instance_weclapp, inventar):
        # mappen der Werte aus device und inventar (TagIdeasy) zu den Pflichtfeldern für Weclapp
        df_mapping = pd.DataFrame.from_dict(instance_weclapp)
        df_mapping.set_index("id", inplace=True)
        # Version-Spalte löschen, da dieser Wert nicht geupdatet werden darf bei WeClapp (Fehlermeldung)
        df_mapping.drop('version', axis=1, inplace=True)
        # Liste von Ids [Artikelnummer, index in inventar-list, WeClapp-Id]
        for ids in article_ids:
            custom_attributes = df_mapping.loc[ids[2]]["customAttributes"]
            try:
                self.update_custom_fields(
                    inventar[ids[1]], custom_attributes[1])
            except:
                self.add_custom_fields(inventar[ids[1]], custom_attributes)
        return df_mapping

    # Prüffelder aktualisieren
    def update_custom_fields(self, inventar, custom_attributes):
        custom_attributes[0]["dateValue"] = inventar["Datum"]
        custom_attributes[1]["stringValue"] = inventar["name"]
        custom_attributes[2]["stringValue"] = inventar["Mängel"]
        custom_attributes[3]["stringValue"] = inventar["accept"]
        custom_attributes[5]["dateValue"] = inventar["nächstes Prüfdatum"]

    # Prüffelder erstellen, falls noch keine vorhanden sind
    def add_custom_fields(self, inventar, custom_attributes):
        custom_attributes[0]["dateValue"] = inventar["Datum"]
        custom_attributes[1]["stringValue"] = inventar["name"]
        custom_attributes[2]["stringValue"] = inventar["Mängel"]
        custom_attributes[3]["stringValue"] = inventar["accept"]
        custom_attributes[5]["dateValue"] = inventar["nächstes Prüfdatum"]

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
    test()