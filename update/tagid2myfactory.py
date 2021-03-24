import pandas as pd
import numpy as np
import json
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import requests
import xmltodict
from fpdf import FPDF
from datetime import date, datetime
from api.myfactory import *
from datetime import datetime, date, timezone

def test():
    mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"
    auth = {
        'username': 'HB',
        'password': 'HB'
    }
    client = MongoClient(mongo_url)
    updateMyFactory = UpdateMyFactory(url, auth, client)
    updateMyFactory.update(0)

class UpdateMyFactory():
    """
    Stellt eine Udatefunktion für MyFactory zur Verfügung. Prüfberichte aus dem Prüfmanagementsystem können so nach MyFactory geladen werden. 
    Da die MyFactory API keinen POST-Requests erlaubt wird als output ein PDF des Prüfberichts erstellt.

    :param str url: gültige Zugangsurl zu Dynamics.
    :param dict auth: Authentifizierungsdaten Form: {"username": string, "password": string }
    :param str mongo_url: URL zur verwendeten MongoDB
    """   

    def __init__(self, url, auth, client):             
        #self.client = pymongo.MongoClient(mongo_url)
        self.client = client
        self.url = url
        self.auth = auth

#TODO: aktuelle Update zeit einbauen
    def update(self,  client, last_update_time = 0, actual_update_time = 0):
        """
        :return: pdf mit Prüfberichten
        
        """


        self.last_update_time = last_update_time
        

        # aktuelle update Zeit speichern
        now = datetime.now()
        # self.update_time = now.strftime("%Y%m%d_%H:%M:%S")
        self.update_time = int(now.replace(tzinfo=timezone.utc).timestamp()) * 1000 
          
        # Instatiate MyFactory-API
        myFactoryAPI = MyFactoryAPI(self.url, self.auth)

        # Inventar und Device Liste von TagIdeasy erhalten
        # inventar, device = get_tagideasy()
        inventar = self.get_tagideasy(client)

        # Erstellen einer Liste aus Artikelnummer und Index für alle Prüfberichte in TagIdeasy
        tagid_ids = [[instance["Artikelnummer"],
                          inventar.index(instance)] for instance in inventar]

        # Relevante Artikel (Geräte) aus MyFactory laden (get-Request)
        myfactory_names = self.get_articel(
            tagid_ids, myFactoryAPI)
        
        if len(self.ids) == 0:
            # TODO. quti testen mit JobScheduler
            # raise Exception("Es gibt keine zu aktualisierenden Artikel")
            return [], False

        # Werte aus Prüfbericht werden als PDF dargestellt und in /output geladen
        info_success = self.map_attributes(
            myfactory_names, inventar)
        
        pdf_created = len(self.ids)
        return  info_success, pdf_created

    # 1) Get Artikel von TagIdeasy, welche geändert werden sollen
    def get_tagideasy(self, client_mongo):
        # Alle Prüfberichte erhalten, welche Zeit dem letzten Update im Prüfmanagement erstellt wurden.
        data = []
        db = self.client['Prüfberichte']
        col = db['Prüfberichte']
        for doc in col.find({"Datum": {"$gt": self.last_update_time}}):
        #for doc in col.find({"Datum": {"$gt": 0}}):
            data.append(doc)
        return data

    # 2) Get-Request der Artikel um die ids der zu updatenden Geräte zu erhalten
    def get_articel(self, tagid_ids, myFactoryAPI):
        # Abrufen aller Artikel
        article_all = myFactoryAPI.get_request()
        article = article_all["feed"]
        # Aussortieren der nicht zu updatenden Artikel
        article_name = []
        article_update = []
        # article_ = []
        for instance in article["entry"]:
            # Liste von Ids [Artikelnummer, index in inventar-list]
            instance_attributes = instance["content"]["m:properties"]
            for i, value in enumerate(tagid_ids):
                if "A0" + str(value[0]) == str(instance_attributes["d:Artikelnummer"]):
                    id = tagid_ids[i]
                    instance_id = instance_attributes['d:PK_ArtikelID']["#text"]
                    instance_article_number = "A0" + id[0]
                    instance_name = instance_attributes['d:Bezeichnung']
                    id = id + [instance_id, instance_article_number]
                    # id: [Artikelnummer, index in Inventar-Liste, id MyFactory , Artikelnummer-MyFactory]
                    article_name.append(instance_name)
                    article_update.append(id)
        self.ids = article_update
        return  article_name

    # 3) mappen der zu ändernden Attribute
    def map_attributes(self, instance_myfactory, inventars):
        # mappen der Werte von TagIdeasy zu den Feldern des PDFs für MyFactory
        pdf = FPDF()
        for i in range(len(instance_myfactory)):
            pos_inventars = self.ids[i][1]
            Prüfdatum = inventars[pos_inventars]["Datum"]
            name = inventars[pos_inventars]["name"]
            maengel = inventars[pos_inventars]["Mängel"]
            accept = str(inventars[pos_inventars]["accept"])
            next_inspection = str(inventars[pos_inventars]["nächstes Prüfdatum"])
            id_myfactory = str(self.ids[i][2])
            Artikelnummer = str(self.ids[i][0])
            Artikelnummer_MyFactory = str(self.ids[i][3])
            artikel_name = instance_myfactory[i]
            # Prüftext = "Prüfbericht: \n Prüfdatum: " + Prüfdatum + "\n Mängel: " + maengel + \
            #     " \n Prüfung bestanden: " + accept + "\n Nächster Prüftermin: " + next_inspection
        
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            pdf.cell(200, 10, txt="Pdf erstellt am:  " + str(datetime.fromtimestamp(self.update_time / 1e3)),
                    ln=1, align='C'),
            pdf.cell(200, 10, txt="Artikelnummer TagIdeasy: " + str(Artikelnummer),
                    ln=1, align='C'),
            pdf.cell(200, 10, txt="Artikelnummer MyFactory: " + str(Artikelnummer_MyFactory),
                    ln=1, align='C'), 
            pdf.cell(200, 10, txt="Id MyFactory: " + str(id_myfactory),
                    ln=1, align='C'),  
            pdf.cell(200, 10, txt="Geprüfte Anlage: " + artikel_name,
                    ln=1, align='C'),  
            pdf.cell(200, 10, txt="-------------------------------------------------------------",
                    ln=1, align='C')                 
            pdf.cell(200, 10, txt="Prüfbericht:",
                    ln=1, align='C')
            pdf.cell(200, 10, txt="Prüfer: " + name,
                    ln=1, align='C'),  
            pdf.cell(200, 10, txt="Prüfdatum: " + str(datetime.fromtimestamp(int(Prüfdatum) / 1e3)),
                    ln=2, align='C')
            pdf.cell(200, 10, txt="Mängel: " + maengel,
                    ln=2, align='C')
            pdf.cell(200, 10, txt="Prüfung bestanden: " + accept,
                    ln=2, align='C')
            pdf.cell(200, 10, txt="Nächster Prüftermin: " + str(datetime.fromtimestamp(int(next_inspection) / 1e3)),
                    ln=2, align='C')

            pdf.output("update/output/" + str(Prüfdatum) + "_" + Artikelnummer_MyFactory  + "_myFactory_Prüfbericht.pdf")

        return True


if __name__ == "__main__":
    test()


    #requests.request("POST", uploadurl, auth=(auth['username'], auth['password']))
