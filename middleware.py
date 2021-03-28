import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
from api.weclapp import *
from update.tagid2weclapp import UpdateWeClapp
from update.tagid2myfactory import UpdateMyFactory
from update.tagid2dynamics import UpdateDynamics
from move_devices. move_tagid_weclapp import MoveTagidWeclapp
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timezone
import logging

def test():
    middlewareControl = MiddlewareControl()
    middlewareControl.init_updates()

class MiddlewareControl():
    """
    Klasse welche Methoden zur Verfügung stellt, die die Konfiguration der Middleware umsetzen.
    """
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # init Database
        mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        try:
            self.client = MongoClient(mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")
        # erp, time_intervall, time_unit, device_export = self.init_config(self.client)
        # self.erp = erp
        # self.time_intervall = time_intervall
        # self.time_unit = time_unit
        # self.device_export = device_export
        self.init_config(self.client)
        
       
    def init_interval_job(self):
        '''
        Job initialisieren, welcher in festen Intervallen durchgeführt wird
        '''
        #TODO: Job Sekundenzeit übergeben
        self.scheduler.add_job(self.job_interval_updates,
                               "interval", seconds=self.time_intervall)

    def job_interval_updates(self):
        print("job1 done")
        self.init_updates()

    def init_updates(self):
        """
        Update eines ERP Systems initialisieren
        """
        # mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        # client = MongoClient(mongo_url)

        # Variablen für Update:
        # get configuration decitions of user saved in MongoDB
        
        # letzten Update Zeitpunkt erhalten
        db = self.client['Keys']
        col = db['Updatefreq']
        try:
            last_update_time = list(col.find())[0]
        except:
            last_update_time = 0

        col.delete_many({})
        # Zeitpunkt des aktuellen Updates 
        now = datetime.now()
        actual_update_time = int(now.replace(tzinfo=timezone.utc).timestamp()) * 1000 
        # TODO: 0 zu last_update_time
        # update methode aufrufen
        result, done, ids = self.updates(self.erp, self.client, last_update_time, actual_update_time, self.device_export)
        print(result, done, ids )
        
        col = db['Updatefreq']
        # Update-Zeit speichern in MongoDB
        if done:
            col.insert_one({"time": actual_update_time})
        else:
            col.insert_one({"time": last_update_time})
        # print(result)
        logging.info("Exportierte Anlagen: System: " + self.erp + "; Artikel Nummern: " + str(ids[1]) )
        logging.info("Update: System: " + self.erp + "; Artikel Nummern: " + str(ids[0]) )


    def init_config(self, client_mongo):
        # das ERP-System, welches verwendet wird erhalten. Falls mehrere in der DB wird das zuletzt verwendete übergeben
        db = self.client['Keys']
        col = db['latestsystem']
        system = list(col.find().sort([('_id', -1)]).limit(1))[0]
        self.erp = system["System"]

        # Einstellungen (Zeitintervall und Anlagen-Export erhalten)
        col = db["settings"]
        settings = list(col.find().sort([('_id', -1)]).limit(1))[0]
        self.time_intervall = settings["INTERVALL"]
        self.time_unit = settings["TIME_UNIT"]
        self.device_export = settings["EXPORT"]
        

        # return system["System"], time_intervall, time_unit, export

    def updates(self, system, client_mongo, last_update_time, actual_update_time, device_export):
        """
        Update eines ERP-Systems

        :param system: gewähltes ERP-System durch den Nutzer
        :param client_mongo: MongoDB
        :param last_update_time: letztes Update Datum
        :param actual_update_time: aktuelles Update Datum
        :param device_export: ob ein Anlagen-Export durchgeführt wird und in welche Richttung

        :return result: 2 Dim. Matrix mit Dictionary der Update und Export Funktion
        :return ids: 2 Dim. Matrix mit Liste der Artikelnummern welche upgedatet und exportiert worden sind
        :return done: Boolean, ob Update funktioniert hat
        """
        # TODO: update Funktion für andere ERP Systeme
        db = client_mongo['Keys']
        if system == "dynamics":
            # Authentifizierungsdaten abrufen
            col = db["Key_Dynamics"]
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))[0]
            # init weclapp-Update Klasse
            updateDynamics = UpdateDynamics(
                system_auth["URL"], {"Authorization": system_auth["BasicAuth"]}, client_mongo)
            # update-Methode ausführen
            result, done = updateDynamics.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
            return result, done, updateDynamics.get_article_number()

        elif system == "weclapp":
            # Authentifizierungsdaten abrufen
            col = db['Key_Weclapp']
            try:
                system_auth = list(col.find().sort(
                    [('timestamp', -1)]).limit(1))[0]
            except:
                raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
            url = system_auth["URL"]
            auth = {"AuthenticationToken": system_auth["Password"]}
            # device-export 
            export_result, export_article_number = self.device_export_weclapp(url, auth , device_export)
            # init weclapp-Update Klasse
            updateWeClapp = UpdateWeClapp(url, auth, client_mongo)
            # update-Methode ausführen
            update_result, done = updateWeClapp.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
            update_article_number = updateWeClapp.get_article_number()
            return [update_result, export_result], done, [update_article_number, export_article_number]

        elif system == "xentral":
            col = db['Key_Xentral']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
            return 0, 0

        elif system == "myfactory":
            # Authentifizierungsdaten abrufen
            col = db['Key_MyFactory']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))[0]
            # init MyFactory-Update Klasse
            updateMyFactory = UpdateMyFactory(system_auth["URL"], {"username": system_auth["Username"], "password": system_auth["Password"]}, self.client)
            # update-Methode ausführen
            pdf_created, done = updateMyFactory.update(last_update_time=last_update_time, actual_update_time=actual_update_time)
            return pdf_created, done, 0
        else:
            logging.error("Keine ERP-System spezifiziert" )
            print("Error: No such Erp System in Database")

        
    def device_export_weclapp(self, url, auth, device_export):
        if device_export == "tagid_erp":
            moveTagidWeclapp = MoveTagidWeclapp(url,auth)
            ids, result = moveTagidWeclapp.export()
        elif device_export == "erp_tagid":
            pass
        else:
            return ["No Export"], ["No Export"]
        return result, ids



if __name__ == "__main__":
    test()
