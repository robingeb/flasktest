import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
# from api.weclapp import *
from update.tagid2weclapp import UpdateWeClapp
from update.tagid2myfactory import UpdateMyFactory
from update.tagid2dynamics import UpdateDynamics
from update.tagid2xentral import UpdateXentral
from move_devices.move_tagid_weclapp import MoveTagidWeclapp
from move_devices.move_weclapp_tagid import MoveWeclappTagid
from move_devices.move_dynamics_tagid import MoveDynamicsTagid
from move_devices.move_tagid_dynamics import MoveTagidDynamics
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timezone
import logging

def test_middleware():
    middlewareControl = MiddlewareControl()
    middlewareControl.init_execution()

class MiddlewareControl():
    """
    Klasse welche Methoden zur Verfügung stellt, die die Konfiguration der Middleware umsetzen.
    """
    def __init__(self):
        # init Scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.export_class = None
        self.update_class = None

        # init Database
        mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
        try:
            self.client = MongoClient(mongo_url)
        except:
            raise Exception("Error: Zugriff auf MongoDB nicht möglich")
        
        # Konfigurations-Variablen
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
        print("job initialisiert")
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
        try:
            last_update_time = list(col.find().sort([('_id', -1)]).limit(1))[0]["time"]
        except:
            last_update_time = 0

        # Zeitpunkt des aktuellen Updates 
        now = datetime.now()
        actual_update_time = int(now.replace(tzinfo=timezone.utc).timestamp()) * 1000 

        # durchführen eines Job-interfalls
        result, ids, done = self.execute_job(self.erp, last_update_time, actual_update_time, self.update_class, self.export_class)
        print(result, ids)
        
        
        # Update-Zeit speichern in MongoDB
        if done:
            col.insert_one({"time": actual_update_time})

        # Logging der Ergebnisse
        logging.info("Exportierte Anlagen: System: " + self.erp + "; Richtung: " + self.device_export + "; Artikel Nummern: " + str(ids[0]) )
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

        # Init notwendige Klassen für Export und Update in Abhängigkeit zu Nutzer-Konfiguration
        if self.erp == "dynamics":
            # Authentifizierungsdaten abrufen
            col = db["Key_Dynamics"]
            try:
                system_auth = list(col.find().sort(
                    [('_id', -1)]).limit(1))[0]
            except:
                raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
            url = system_auth["URL"]
            auth = {"Authorization": system_auth["BasicAuth"]}
            # init Dynamics-Update Klasse
            update_class = UpdateDynamics(
                url,auth , self.client)
            # init Dynamics-Export Klasse falls benötigt
            if self.device_export == "tagid_erp":
                export_class = MoveTagidDynamics(url,auth)
            elif self.device_export == "erp_tagid":
                export_class = MoveDynamicsTagid(url, auth)            
            else:
                export_class = None        

            self.update_class = update_class
            self.export_class = export_class
        elif self.erp == "weclapp":
            # Authentifizierungsdaten abrufen
            col = db["Key_Weclapp"]
            try:
                system_auth = list(col.find().sort(
                    [('_id', -1)]).limit(1))[0]
            except:
                raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
            url = system_auth["URL"]
            auth = {"AuthenticationToken": system_auth["Password"]}
            # init Dynamics-Update Klasse
            update_class = UpdateWeClapp(url, auth, self.client)
            # init Dynamics-Export Klasse falls benötigt
            if self.device_export == "tagid_erp":
                export_class = MoveTagidWeclapp(url,auth)
            elif self.device_export == "erp_tagid":
                export_class = MoveWeclappTagid(url, auth)            
            else:
                export_class = None        

            self.update_class = update_class
            self.export_class = export_class
        elif self.erp == "xentral":
            # Authentifizierungsdaten abrufen
            col = db["Key_Xentral"]
            try:
                system_auth = list(col.find().sort(
                    [('_id', -1)]).limit(1))[0]
            except:
                raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
            url = system_auth["URL"]
            auth = {"username": system_auth["Username"], "password": system_auth["Password"]}
            # init Dynamics-Update Klasse
            update_class = UpdateXentral(url, auth, self.client)                
            self.update_class = update_class
        elif self.erp == "myfactory":
            # Authentifizierungsdaten abrufen
            col = db["Key_MyFactory"]
            try:
                system_auth = list(col.find().sort(
                    [('_id', -1)]).limit(1))[0]
            except:
                raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
            url = system_auth["URL"]
            auth = {"username": system_auth["Username"], "password": system_auth["Password"]}
            # init Dynamics-Update Klasse
            update_class = UpdateMyFactory(url, auth, self.client)                
            self.update_class = update_class

            


        # return system["System"], time_intervall, time_unit, export

    def execute_job(self, system, last_update_time, actual_update_time, updateClass, exportClass = None):
        """
        Update eines ERP-Systems

        :param system: gewähltes ERP-System durch den Nutzer
        :param last_update_time: letztes Update Datum
        :param actual_update_time: aktuelles Update Datum
        :param updateClass: Klasse des zu updatenden Systems
        :param exportClass: Klasse zum Exportieren der Anlagen

        :return result: 2 Dim. Matrix mit Dictionary der Update und Export Funktion
        :return ids: 2 Dim. Matrix mit Liste der Artikelnummern welche upgedatet und exportiert worden sind
        :return done: Boolean, ob Update funktioniert hat
        """
        if system == "dynamics" or system == "weclapp":
            # export
            export_result, export_article_number = self.device_export_dynamics(exportClass)        
                
            # update-Methode ausführen
            update_result, done = updateClass.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
            update_article_number = updateClass.get_article_number()
            return [export_result, update_result], [export_article_number, update_article_number], done
        if system == "xentral" or system == "myfactory":
            # init MyFactory-Update Klasse
            # updateXentral = UpdateXentral(system_auth["URL"], {"username": system_auth["Username"], "password": system_auth["Password"]}, self.client)
            # update-Methode ausführen
            pdf_created, article_numbers, done = updateClass.update(last_update_time=last_update_time, actual_update_time=actual_update_time)
            
            return [ "kein Export", pdf_created], ["kein Export", article_numbers], done



    #     # TODO: update Funktion für andere ERP Systeme
    #     db = self.client['Keys']
    #     if system == "dynamics":
    #         # export
    #         export_result, export_article_number = self.device_export_dynamics(exportClass)        
            
    #         # update-Methode ausführen
    #         update_result, done = updateClass.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
    #         update_article_number = updateClass.get_article_number()
    #         return [export_result, update_result], [export_article_number, update_article_number], done

    #     elif system == "weclapp":
    #         # Authentifizierungsdaten abrufen
    #         # col = db['Key_Weclapp']
    #         # try:
    #         #     system_auth = list(col.find().sort(
    #         #         [('_id', -1)]).limit(1))[0]
    #         # except:
    #         #     raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
    #         # url = system_auth["URL"]
    #         # auth = {"AuthenticationToken": system_auth["Password"]}
    #         # device-export 
    #         export_result, export_article_number = self.device_export_weclapp(device_export)
    #         # init weclapp-Update Klasse
    #         updateWeClapp = UpdateWeClapp(url, auth, self.client)
    #         # update-Methode ausführen
    #         update_result, done = updateWeClapp.update(last_update_time=last_update_time, actual_update_time = actual_update_time)
    #         update_article_number = updateWeClapp.get_article_number()
    #         return [export_result, update_result], [export_article_number, update_article_number], done

    #     elif system == "xentral":
    #         # kein Export implementiert, da kein PUSH-Request möglich
    #         # Authentifizierungsdaten abrufen
    #         col = db['Key_Xentral']
    #         try:
    #             system_auth = list(col.find().sort(
    #                 [('_id', -1)]).limit(1))[0]
    #         except:
    #             raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
    #         # init MyFactory-Update Klasse
    #         updateXentral = UpdateXentral(system_auth["URL"], {"username": system_auth["Username"], "password": system_auth["Password"]}, self.client)
    #         # update-Methode ausführen
    #         pdf_created, article_numbers, done = updateXentral.update(last_update_time=last_update_time, actual_update_time=actual_update_time)
            
    #         return [ "kein Export", pdf_created], ["kein Export", article_numbers], done

    #     elif system == "myfactory":
    #         # kein Export implementiert, da kein PUSH-Request möglich
    #         # Authentifizierungsdaten abrufen
    #         col = db['Key_MyFactory']
    #         try:
    #             system_auth = list(col.find().sort(
    #                 [('_id', -1)]).limit(1))[0]
    #         except:
    #             raise Exception("Error: Kein Eintrag der Authentifizierungsdaten für weclapp in MongoDB" )
    #         # init MyFactory-Update Klasse
    #         updateMyFactory = UpdateMyFactory(system_auth["URL"], {"username": system_auth["Username"], "password": system_auth["Password"]}, self.client)
    #         # update-Methode ausführen
    #         pdf_created, article_numbers, done = updateMyFactory.update(last_update_time=last_update_time, actual_update_time=actual_update_time)
            
    #         return [ "kein Export", pdf_created], ["kein Export", article_numbers], done
    #     else:
    #         logging.error("Keine ERP-System spezifiziert" )
    #         print("Error: No such Erp System in Database")

        
    # def device_export_weclapp(self, url, auth, device_export):
    #     print("weclapp")
    #     if device_export == "tagid_erp":
    #         moveTagidWeclapp = MoveTagidWeclapp(url,auth)
    #         ids, result = moveTagidWeclapp.export()
    #     elif device_export == "erp_tagid":
    #         moveWeclappTagid = MoveWeclappTagid(url, auth)
    #         ids, result = moveWeclappTagid.export(self.article_number_range)
    #     else:
    #         return ["Kein Export"], ["Kein Export"]
    #     return result, ids

    def device_export_dynamics(self, device_export):
        if device_export != None: 
            if self.device_export == "erp_tagid":           
                ids, result = device_export.export(self.article_number_range)
            else:
                ids, result = device_export.export()
        else:
            return ["Kein Export"], ["Kein Export"]
        return result, ids

    # def device_export_dynamicst(self, url, auth, device_export):
    #     print("dynamics")
    #     if device_export == "tagid_erp":
    #         moveTagidDynamics = MoveTagidDynamics(url,auth)
    #         ids, result = moveTagidDynamics.export()
    #         pass
    #     elif device_export == "erp_tagid":
    #         moveDynamicsTagid = MoveDynamicsTagid(url,auth)
    #         ids, result = moveDynamicsTagid.export(self.article_number_range)
    #     else:
    #         return ["Kein Export"], ["Kein Export"]
    #     return result, ids


if __name__ == "__main__":
    test_middleware()
