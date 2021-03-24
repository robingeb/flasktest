import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
from api.weclapp import *
from update.tagid2weclapp import UpdateWeClapp
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timezone
# import logging

def test():
    middlewareControl = MiddlewareControl()
    middlewareControl.init_updates()

class MiddlewareControl():
    """
    Klasse welche Methoden zur Verfügung stellt, die die Konfiguration der Middleware umsetzen.
    """
    def __init__(self):
        #self.scheduler = BackgroundScheduler()
        #self.scheduler.start()

        # init Database
        mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        try:
            self.client = MongoClient(mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")
        
       
    def init_interval_job(self):
        '''
        Job initialisieren, welcher in festen Intervallen durchgeführt wird
        '''
        #TODO: Job Sekundenzeit übergeben
        self.scheduler.add_job(self.job_interval_updates,
                               "interval", seconds=30)

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
        erp, last_update_time = self.get_config(self.client)
        # Zeitpunkt des aktuellen Updates 
        now = datetime.now()
        actual_update_time = int(now.replace(tzinfo=timezone.utc).timestamp()) * 1000 
        # TODO: 0 zu last_update_time
        # update methode aufrufen
        result, done, update_ids = self.updates(erp, self.client, 0, actual_update_time)

        db = self.client['Keys']
        col = db['Updatefreq']
        # Update-Zeit speichern in MongoDB
        if done:
            col.insert_one({"time": actual_update_time})
        else:
            col.insert_one({"time": last_update_time})
        # print(result)
        
        # logging.info("Update: System: " + erp + "; Artikel Nummern: " + str(update_ids))


    def get_config(self, client_mongo):
        # get the last used erp-System
        db = self.client['Keys']
        col = db['latestsystem']
        system = list(col.find().sort([('timestamp', -1)]).limit(1))[0]

        # letzten Update Zeitpunkt erhalten
        col = db['Updatefreq']
        try:
            update_frequ = list(col.find())[0]
        except:
            return system["System"], 0
        col.delete_many({})
        return system["System"], update_frequ["time"]

    def updates(self, system, client_mongo, last_update_time, actual_update_time):
        # get erp-System authentification data and start update function of the System
        # TODO: update Funktion für andere ERP Systeme
        db = client_mongo['Keys']
        if system == "dynamics":
            col = db["Key_Dynamics"]
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
            return 0, 0
        elif system == "weclapp":
            # letzten Zeitstempel
            col = db['Key_Weclapp']
            system_auth = list(col.find().sort(
                [('timestamp', -1)]).limit(1))[0]
            # init weclapp-Update Klasse
            updateWeClapp = UpdateWeClapp(
                system_auth["URL"], {"AuthenticationToken": system_auth["Password"]}, client_mongo)
            result, done = updateWeClapp.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
            return result, done, updateWeClapp.get_article_number()

        elif system == "xentral":
            col = db['Key_Xentral']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
            return 0, 0
        elif system == "myfactory":
            col = db['Key_MyFactory']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
            return 0, 0
        else:
            print("Error: No such Erp System in Database")


if __name__ == "__main__":
    test()
