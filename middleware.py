import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
# from api.weclapp import *
from update.tagid2weclapp import UpdateWeClapp
from update.tagid2myfactory import UpdateMyFactory
from update.tagid2dynamics import UpdateDynamics
from move_devices.move_tagid_weclapp import MoveTagidWeclapp
from move_devices.move_weclapp_tagid import MoveWeclappTagid
from move_devices.move_dynamics_tagid import MoveDynamicsTagid
from move_devices.move_tagid_dynamics import MoveTagidDynamics
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
        # init Scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # init Database
        mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        try:
            self.client = MongoClient(mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")
        
        # Konfiguration
        self.erp = ""
        self.time_intervall = 0
        self.time_unit = ""
        self.device_export = ""
        self.article_number_range = [0, 0]
        try:
            self.init_config()
        except:
            pass
        self.activ = False

    def get_config(self): 
        return [self.erp, self.device_export, self.time_intervall, self.time_unit, self.article_number_range]

    def get_activ(self):
        return self.activ
        
       
    def init_interval_job(self):
        '''
        Job initialisieren, welcher in festen Intervallen durchgeführt wird
        '''
        if self.time_unit == "seconds":
            self.activ = True
            self.scheduler.add_job(self.job_interval_updates,
                                "interval", seconds=self.time_intervall, id = "job_interval")
        elif self.time_unit == "minutes":
            self.activ = True
            self.scheduler.add_job(self.job_interval_updates,
                                "interval", minutes=self.time_intervall, id = "job_interval")
        elif self.time_unit == "hours":
            self.activ = True
            self.scheduler.add_job(self.job_interval_updates,
                                "interval", hours=self.time_intervall, id = "job_interval")
        elif self.time_unit == "days":
            self.activ = True
            self.scheduler.add_job(self.job_interval_updates,
                                "interval", days=self.time_intervall, id = "job_interval")

    def remove_job(self, name):
        self.scheduler.remove_job(name)
    
    def get_job(self, name):
        return self.scheduler.get_job(name)

    def job_interval_updates(self):
        print("job Update initialisiert")
        self.init_execution()

    # def job_interval_updates_pause(self):
    #     print("job1 done")
    #     self.scheduler.resume_job()

    def init_execution(self):
        """
        Update eines ERP Systems initialisieren
        """
        
        # letzten Update Zeitpunkt erhalten
        db = self.client['Keys']
        col = db['Updatefreq']
        # try:
        #     last_update_time = list(col.find())[0]
        # except:
        #     last_update_time = 0
        try:
            last_update_time = list(col.find().sort([('_id', -1)]).limit(1))[0]["time"]
        except:
            last_update_time = 0

        #col.delete_many({})
        # Zeitpunkt des aktuellen Updates 
        now = datetime.now()
        actual_update_time = int(now.replace(tzinfo=timezone.utc).timestamp()) * 1000 
        # TODO: 0 zu last_update_time
        # durchführen eines Job-interfalls
        result, ids, done = self.execute_job(self.erp, self.client, last_update_time, actual_update_time, self.device_export)
        print(result, ids, done )
        
        
        # Update-Zeit speichern in MongoDB
        if done:
            col.insert_one({"time": actual_update_time})
        # else:
        #     col.insert_one({"time": last_update_time})
        # print(result)
        logging.info("Exportierte Anlagen: System: " + self.erp + "; Artikel Nummern: " + str(ids[0]) )
        logging.info("Update: System: " + self.erp + "; Artikel Nummern: " + str(ids[1]) )


    def init_config(self):
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
        # Wenn Anlagen-Export von ERP nach Tagid kann Artikel-Nummer Wertebereich eingschrängt werden.
        if self.device_export == "erp_tagid":
            self.article_number_range = settings["ARTICLENUMBERRANGE"]
            if self.article_number_range == ["",""]:
                self.article_number_range = [0,0]
        else:
            self.article_number_range = [0,0]

        # return system["System"], time_intervall, time_unit, export

    def execute_job(self, system, client_mongo, last_update_time, actual_update_time, device_export):
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
            return [export_result, update_result], [export_article_number, update_article_number], done

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
            pdf_created, article_numbers, done = updateMyFactory.update(last_update_time=last_update_time, actual_update_time=actual_update_time)
            
            return [ "kein Export", pdf_created], ["kein Export", article_numbers], done
        else:
            logging.error("Keine ERP-System spezifiziert" )
            print("Error: No such Erp System in Database")

        
    def device_export_weclapp(self, url, auth, device_export):
        if device_export == "tagid_erp":
            moveTagidWeclapp = MoveTagidWeclapp(url,auth)
            ids, result = moveTagidWeclapp.export()
        elif device_export == "erp_tagid":
            moveWeclappTagid = MoveWeclappTagid(url, auth)
            ids, result = moveWeclappTagid.export(self.article_number_range)
        else:
            return ["No Export"], ["No Export"]
        return result, ids

    def device_export_dynamics(self, url, auth, device_export):
        #TODO Skripte funktionieren noch nicht
        if device_export == "tagid_erp":
            moveTagidDynamics = MoveTagidDynamics(url,auth)
            ids, result = moveTagidDynamics.export()
            pass
        elif device_export == "erp_tagid":
            moveDynamicsTagid = MoveDynamicsTagid(url,auth)
            ids, result = moveTagidDynamics.export()
        else:
            return ["No Export"], ["No Export"]
        return result, ids


if __name__ == "__main__":
    test()
