from flask import Flask, render_template, url_for, render_template, request, redirect
from flask_forms import NameForm, articleForm, choiceform, erpformweclapp, erpformdynamics, erpformmyfactory, erpformxentral, articlehomeForm
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True

app.config["MONGO_URI"] = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
mongo = PyMongo(app)
client = pymongo.MongoClient(
    "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")


@app.route('/', methods=['POST'])
def home():
    name = None
    form = articlehomeForm()

    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('formular_home.html', form=form, name=name)


@app.route('/article', methods=['GET', 'POST'])
def index():

    name = None
    form = articleForm()

    if form.validate_on_submit():

        Artikelnr = str(form.Artikelnummer.data)
        return redirect(url_for('signup', Artikelnr=Artikelnr))

    return render_template('article.html', form=form, name=name)


@app.route('/formular/<string:Artikelnr>', methods=['GET', 'POST'])
def signup(Artikelnr):
    name = None
    form = NameForm()
    db = client['Prüfberichte']
    col = db['Prüfberichte']

    if form.validate_on_submit():

        # ID des Prüfers (INT)
        # WIRD NOCH NICHT ÜBERTRAGEN
        ID = form.ID.data
        ID = str(ID)

        # nächstes Prüfdatum übertragen:
        # date2 aus Formular holen: date zu datetime konvertieren -> datetime zu unixtime (float) konvertieren -> float in int konvertieren (um Nachkommastellen zu entfernen) -> int in String konvertireren und 3 nullen dranhängen
        date2 = form.date2.data
        dt2 = datetime.combine(date2, datetime.min.time())

        dt = form.date1.data

        # Var timestamp wird in payload benutzt
        timestamp = dt2.replace(tzinfo=timezone.utc).timestamp()
        timestamp = int(timestamp)
        timestamp = str(timestamp) + "000"
        timestamp = int(timestamp)

        timestamp2 = dt.replace(tzinfo=timezone.utc).timestamp()
        timestamp2 = int(timestamp2)
        timestamp2 = str(timestamp2) + "000"
        timestamp2 = int(timestamp2)
        print(timestamp2)

        # Name des Prüfers (String)
        name = form.name.data

        #Mängel (Textfield)
        mängel = form.mängel.data

        # Gerät bestanden (bool)
        accept = form.accept.data
        accept = str(accept)

        price = "1"

        datasets = col.insert_one({"Mängel": str(mängel), "name": str(
            name), "accept": accept, "Datum": timestamp2, "nächstes Prüfdatum": timestamp, "Artikelnummer": str(Artikelnr)})

        #payload = "\r\n{\r\n    \"classification\": \r\n        {\"company_id\": \"BDx2AOwdcfwBI9Grb52w\" ,\r\n        \"department_id\": \"34RxZCwUMYG9WXA526Qz\" ,\r\n        \"place_id\": \"YFVj90X1OPPPSCejK0Ra\" },\r\n    \"core\": \r\n        {\"articel_id_buyer\": \""+Artikelnr+"\",\r\n         \"build_year\": \"2019\" ,\r\n         \"inventory_number\": \"123\" ,\r\n         \"price\": \""+price+"\" ,\r\n         \"serial_number\": \""+Artikelnr+"\" ,\r\n         \"Startup_date\": \"16. Dezember 2020 um 10:41:33 UTC+1\" ,\r\n         \"supplier_id\": \"boHE2bqk1VzJ4tBANsH8\" },\r\n    \"historical_data\":\r\n        {\"created_at\": \"16. Dezember 2020 um 10:41:33 UTC+1\" ,\r\n         \"created_by\": \"HKyUyCuVj0g12htOsAPmGCcffBq2\" ,\r\n         \"updated_at\": \"16. Dezember 2020 um 10:41:33 UTC+1\" ,\r\n         \"updated_by\": \"HKyUyCuVj0g12htOsAPmGCcffBq2\" },\r\n    \"identifiers\":\r\n         {\"barcode\": \"1234\" ,\r\n          \"device_d\": \"1234\" ,\r\n          \"qr\": \"1234\" ,\r\n          \"rfid\": \"1234\" },\r\n    \"media\":\r\n        {\"attachments\": [\r\n        {\r\n        \"name\": \""+name+"\", \r\n        \"Datum\": "+timestamp2+",\r\n        \"nächstes Prüfdatum\": "+timestamp+"\r\n        \"mängel\": \""+mängel+"\",\r\n        \"accept\": "+accept+",\r\n        }\r\n        ]},\r\n    \"status\":\r\n        {\"archived\": true}\r\n}"

        # print(payload)
        print("erfolgreich")
        #print(requests.request("PUT", url, headers=headers, data=payload))
        return 'geht'

    else:
        print('nicht erfolgreich')

    return render_template('signup.html', form=form, name=name)


if __name__ == '__main__':
    app.run(debug=True)
