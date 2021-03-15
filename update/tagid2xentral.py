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
from api.xentral import *

#TODO: Xentral nicht zugreifbar

def test():
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

    def __init__(self, url, auth, mongo_url):             
        self.client = pymongo.MongoClient(mongo_url)
        self.url = url
        self.auth = auth
        

    def update(self):
        """
        :return: pdf mit Prüfberichten
        
        """
        pdf = FPDF()     

        xentralApi = XentralAPI(self.url, self.auth)
        article_all = xentralApi.get_request()

        db = self.client['Prüfberichte']
        col = db['Prüfberichte']

        last_update = 0
        Prüfbericht = []
        Pruefbericht = []

        for doc in col.find({"Datum": {"$gt": last_update}}):
            Prüfbericht.append(doc)

        Prüfbericht = str(Prüfbericht)
        Prüfbericht = Prüfbericht.split(",")

        for x in Prüfbericht:
            z = x.split(": ")
            Pruefbericht.append(z[1])

        print(Pruefbericht)


        Prüfdatum = Pruefbericht[4]
        name = Pruefbericht[2]
        maengel = Pruefbericht[1]
        accept = str(Pruefbericht[3])
        next_inspection = str(Pruefbericht[5])
        Prüftext = "Prüfbericht: \n Prüfdatum: " + Prüfdatum + "\n Mängel: " + maengel + \
            " \n Prüfung bestanden: " + accept + "\n Nächster Prüftermin: " + next_inspection
        # print(Pruefbericht[6])

        Aritkelnummer = Pruefbericht[6]

        # print(article_all)
        #

        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt="Prüfbericht:",
                ln=1, align='C')

        pdf.cell(200, 10, txt="Prüfdatum: " + str(datetime.fromtimestamp(int(Prüfdatum) / 1e3)),
                ln=2, align='C')
        pdf.cell(200, 10, txt="Mängel: " + maengel,
                ln=2, align='C')
        pdf.cell(200, 10, txt="Prüfung bestanden: " + accept,
                ln=2, align='C')
        pdf.cell(200, 10, txt="Nächster Prüftermin: " + str(datetime.fromtimestamp(int(next_inspection) / 1e3)),
                ln=2, align='C')


        print(type(next_inspection))
        print(type(Prüfdatum))
        print(Prüfdatum)
        print(next_inspection)
        pdf.output("update/output/xentral_" + str(Prüfdatum) + "_Prüfbericht.pdf")

        uploadurl = "http://132.187.226.135/www/api//index.php/v1/artikel" + \
            str(Aritkelnummer)+"/document/Prüfbericht.pdf"

if __name__ == "__main__":
    test()
