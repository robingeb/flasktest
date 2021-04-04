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
from datetime import datetime, date, timezone
# from api.xentral import *


def test_tagid2xentral():
    url = "http://132.187.226.135/www/api//index.php/v1/artikel"
    auth = {
        'username': 'Alpi',
        'password': 'Alpi'
    }
    mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    updateXentral = UpdateXentral(url, auth, mongo_url)
    updateXentral.update()

class UpdateXentral():
    """
    Stellt eine Udatefunktion für Xentral zur Verfügung. Prüfberichte aus dem Prüfmanagementsystem können so nach Xentral geladen werden. 
    Da die Xentral API PUT-Requests nicht erlaubt wird als output ein PDF des Prüfberichts erstellt.

    :param str url: gültige Zugangsurl zu Xentral.
    :param dict auth: Authentifizierungsdaten Form: {"username": string, "password": string}
    :param str mongo_url: URL zur verwendeten MongoDB
    """  

    def __init__(self, url, auth, client):             
        self.client = client
        self.update_time = 0
        self.ids = []
        

    def update(self, last_update_time = 0, actual_update_time = 0):
        """
        Erstellen eines pdfs für alle neuen Prüfberichte

        :return: alle Prüfberichte als pdf
        :return pdf_created: Zahl der erstellten pdfs
        :return ids: Artikel-Nummbern der Anlagen
        :return info_success: Boolscher Wert, ob das erstellen aller pdfs erfolgreich war
        
        """
        # reset
        self.ids = []
        
        self.update_time = actual_update_time

        # Inventar und Device Liste von TagIdeasy erhalten
        inventar = self.get_tagideasy(last_update_time)

        # Erstellen einer Liste aus Artikelnummer und Index für alle Prüfberichte in TagIdeasy
        self.ids = [instance["Artikelnummer"] for instance in inventar]

        if len(self.ids) == 0:
            return [], [], False

        # Werte aus Prüfbericht werden als PDF dargestellt und in /output geladen
        info_success = self.map_attributes(inventar)
        
        pdf_created = len(self.ids)
        
        return  pdf_created, self.ids, info_success
    
    # 1) Get Artikel von TagIdeasy, welche geändert werden sollen
    def get_tagideasy(self, last_update_time):
        # Alle Prüfberichte erhalten, welche Zeit dem letzten Update im Prüfmanagement erstellt wurden.
        data = []
        db = self.client['Prüfberichte']
        col = db['Prüfberichte']
        for doc in col.find({"Datum": {"$gt": last_update_time}}):
        #for doc in col.find({"Datum": {"$gt": 0}}):
            data.append(doc)
        return data
    
    # (Artikel laden von Xentral): wurde ausgelassen, da das System den letzten Monat nicht zur Verfügung stand. 
    # Stattdessen werden alle in tagIdeasy enthaltenen Prüfberichte als PDF exportiert

    # 2) mappen der zu ändernden Attribute
    def map_attributes(self, inventars):
        # mappen der Werte von TagIdeasy zu den Feldern des PDFs für Xentral
        pdf = FPDF()
        for i in range(len(inventars)):
            Prüfdatum = inventars[i]["Datum"]
            name = inventars[i]["name"]
            maengel = inventars[i]["Mängel"]
            accept = str(inventars[i]["accept"])
            next_inspection = str(inventars[i]["nächstes Prüfdatum"])
            Artikelnummer = str(self.ids[i])

             # Erstellen einer PDF-Seite 
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            pdf.cell(200, 10, txt="Pdf erstellt am:  " + str(datetime.fromtimestamp(self.update_time / 1e3)),
                    ln=1, align='C'),
            pdf.cell(200, 10, txt="Artikelnummer: " + str(Artikelnummer),
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

            # Speichern des PDFs in dem Directory: "update/output/"
            pdf.output("update/output/" + str(Prüfdatum) + "_" + self.ids[i]  + "_Xentral_Prüfbericht.pdf")
        return True

if __name__ == "__main__":
    test_tagid2xentral()
