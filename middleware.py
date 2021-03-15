import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
from api.weclapp import *
from update.tagid2weclapp import UpdateWeClapp
from apscheduler.schedulers.background import BackgroundScheduler

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

    def init_interval_scheduler(self):
        '''
        Jobs initialisieren, welcher in festen intervallen durchgeführt wird
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
        mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        client = MongoClient(mongo_url)

        # get configuration decitions of user saved in MongoDB
        erp, update_time = self.get_config(client)
        self.updates(erp, mongo_url, client)

        print(erp)
        print(update_time)
        # print(system_auth)

    def get_config(self, client_mongo):
        # get the last used erp-System
        db = client_mongo['Keys']
        col = db['latestsystem']
        system = list(col.find().sort([('timestamp', -1)]).limit(1))[0]

        # get the update-frequenzy
        col = db['Updatefreq']
        update_frequ = list(col.find().sort([('timestamp', -1)]).limit(1))[0]

        return system["System"], update_frequ["time"]

    def updates(self, system, mongo_url, client_mongo):
        # get erp-System authentification data and start update function of the System
        # TODO: update Funktion für andere ERP Systeme
        db = client_mongo['Keys']
        if system == "dynamics":
            col = db["Key_Dynamics"]
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
        elif system == "weclapp":
            col = db['Key_Weclapp']
            system_auth = list(col.find().sort(
                [('timestamp', -1)]).limit(1))[0]
            updateWeClapp = UpdateWeClapp(
                system_auth["URL"], {"AuthenticationToken": system_auth["Password"]}, mongo_url)
            result = updateWeClapp.update()
            print(result)
        elif system == "xentral":
            col = db['Key_Xentral']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
        elif system == "myfactory":
            col = db['Key_MyFactory']
            system_auth = list(col.find().sort([('timestamp', -1)]).limit(1))
        else:
            print("Error: No such Erp System in Database")


if __name__ == "__main__":
    test()
