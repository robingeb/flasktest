from flask import Flask, render_template, url_for, render_template, request, redirect
from flask_forms import choiceendForm, choicestartForm, NameForm, articleForm, choiceform, erpformweclapp, erpformdynamics, erpformmyfactory, erpformxentral, choicehomeForm
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import logging
# bene: Notwendige imports
#from flask_apscheduler import APScheduler
from middleware import *

# ------------------------------------ INFO -----------------------------------------------------------------------
# Run Button wählen, um Anwendung zu starten
# Local Host öffnen:  http://127.0.0.1:5000/
# Wenn Seite nicht gefunden werden kann, nochmal laden, da Anwendung noch nicht fertig erstellt wurde.
# Anwendung kann geschlossen werden indem strg + c im Terminal eingegeben wird


#------------------------------------- Start Anwendung -----------------------------------------------------------

app = Flask(__name__, template_folder='templates')
# logging instantiate
logging.basicConfig( filename='logs/debug.log', format='%(asctime)s %(name)s %(message)s', level=logging.DEBUG)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True

# initialize Middleware Control Class
middleware = MiddlewareControl()

app.config["MONGO_URI"] = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
mongo = PyMongo(app)
client = pymongo.MongoClient(
    "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")


@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():
    # testen ob  bereits ein Job existiert
    job = middleware.get_job("job_interval")
    
    # test ob Eintrag in der DB
    db = client['Keys']
    col = db['settings']

    # Job restarten, wenn ein Settings eintrage existiert und wenn nicht bereits ein Job läuft
    if col.count != 0 and job == None:
        print ("Job restarted")
        middleware.init_interval_job()    
    return ("nichts")

@app.route('/', methods=['GET', 'POST'])
def homi():
    '''
    Start-Seite der Web-Anwendung. Darstellung der aktuellen Konfiguration. 
    Über Buttons neue Konfiguration erstellen oder aktuelle Konfiguration starten
    '''
    name = None
    form = choicestartForm()
    info = middleware.get_config()
    activ = middleware.get_activ()

    # [0,0] als leere Felder darstellen
    if info[4] == [0,0]:
        info[4] = ["",""]
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('choice_start.html', form=form, name=name, info = info, activ = activ)


@app.route('/system', methods=['GET', 'POST'])
def home():
    '''
    Formular, um allgemeine Einstellungen du definieren (Intervall länge, Anlagen-Export)
    '''
    name = None
    form = choicehomeForm()

    # Settings MongoDB
    db = client['Keys']
    col = db['settings']

    # Wenn ein Job gerade am laufen ist, wird dieser beendet
    if middleware.get_job("job_interval") != None:
        middleware.remove_job("job_interval")

    # Formular für settings
    if form.validate_on_submit():
        time = form.time.data
        time_unit = form.time_unit.data
        export = form.export.data   
        article_number_min = form.article_number_min.data
        article_number_max = form.article_number_max.data 
        # speichern in MongoDB    
        datasets = col.insert_one({"INTERVALL": time, "TIME_UNIT": time_unit, "EXPORT": export, "ARTICLENUMBERRANGE": [article_number_min, article_number_max]})
        return redirect(url_for('choice'))
    return render_template('choice_home.html', form=form, name=name)

@app.route('/choice', methods=['GET', 'POST'])
def choice():
    '''
    Auswahl des verwendeten ERP-Systems [weclapp, Dynamics, MyFactory, Xentral]
    '''
    name = None
    form = choiceform()

    if form.validate_on_submit():
        System = str(form.System.data)       
        return redirect(url_for('erp', System=System))
    return render_template('choice.html', form=form, name=name)

@app.route('/erp/<string:System>', methods=['GET', 'POST'])
def erp(System):
    '''
    Eingeben der API-Zugangsdaten in Abhängigkeit zum verwendeten ERP-System. 
    Middleware wird mit wählen des Submitt-Buttons gestartet
    '''
    name = None
    db = client['Keys']
    col = db['latestsystem']
    datasets = col.insert_one({"System": str(System)})

    if System == 'weclapp':
        form = erpformweclapp()
        col = db['Key_Weclapp']

        if form.validate_on_submit():
            URL = form.URL.data
            Password = form.Password.data

            # speichern in MongoDB
            datasets = col.insert_one(
                {"URL": str(URL), "Password": str(Password)})

            # Middleware mit User-Settings Konfigurieren und Job starten
            middleware.init_config()
            middleware.init_interval_job()
            return redirect(url_for('homi'))
        return render_template('erpweclapp.html', form=form, name=name)

    if System == 'dynamics':
        form = erpformdynamics()
        col = db['Key_Dynamics']

        if form.validate_on_submit():

            BasicAuth = form.BasicAuth.data
            URL = form.URL.data

            # speichern in MongoDB
            datasets = col.insert_one(
                {"URL": str(URL), "BasicAuth": str(BasicAuth)})

            # Middleware mit User-Settings Konfigurieren und Job starten
            middleware.init_config()
            middleware.init_interval_job()
            return redirect(url_for('homi'))
        return render_template('erpdynamics.html', form=form, name=name)

    if System == 'xentral':
        form = erpformxentral()
        col = db['Key_Xentral']

        if form.validate_on_submit():
            Username = form.Username.data
            Password = form.Password.data
            URL = form.URL.data

            # speichern in MongoDB
            datasets = col.insert_one(
                {"URL": str(URL), "Username": str(Username), "Password": str(Password)})

            # Middleware mit User-Settings Konfigurieren und Job starten
            middleware.init_config()
            middleware.init_interval_job()
            return redirect(url_for('homi'))
        return render_template('erpxentral.html', form=form, name=name)

    if System == 'myfactory':
        form = erpformmyfactory()
        col = db['Key_MyFactory']

        if form.validate_on_submit():
            Username = form.Username.data
            Password = form.Password.data
            URL = form.URL.data

            # speichern in MongoDB
            datasets = col.insert_one(
                {"URL": str(URL), "Username": str(Username), "Password": str(Password)})

            # Middleware mit User-Settings Konfigurieren und Job starten
            middleware.init_config()
            middleware.init_interval_job()
            return redirect(url_for('homi'))
        return render_template('erpmyfactory.html', form=form, name=name)
    return 'Das ERP-System wurde nicht gefunden'


if __name__ == '__main__':
    app.run(debug=True)
