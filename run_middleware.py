from flask import Flask, render_template, url_for, render_template, request, redirect
from flask_forms import NameForm, articleForm, choiceform, erpformweclapp, erpformdynamics, erpformmyfactory, erpformxentral, choicehomeForm
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
# import logging
# bene: Notwendige imports
#from flask_apscheduler import APScheduler
from middleware import *



app = Flask(__name__, template_folder='templates')
# logging instantiate
# logging.basicConfig( filename='logs/demo.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True


app.config["MONGO_URI"] = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
mongo = PyMongo(app)
client = pymongo.MongoClient(
    "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")

# initialize Middleware Control Class
middleware = MiddlewareControl()

@app.route('/', methods=['GET', 'POST'])
def home():
    app.logger.info('Processing default request')

    name = None
    form = choicehomeForm()

    db = client['Prüfberichte']
    col = db['Intervall']

    if form.validate_on_submit():

        time = form.time.data
        datasets = col.insert_one({"URL": time})
        return redirect(url_for('choice'))

    return render_template('choice_home.html', form=form, name=name)


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    name = None
    form = choiceform()

    if form.validate_on_submit():
        System = str(form.System.data)

        return redirect(url_for('erp', System=System))

    return render_template('choice.html', form=form, name=name)

@app.route('/erp/<string:System>', methods=['GET', 'POST'])

def erp(System):
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

            datasets = col.insert_one(
                {"URL": str(URL), "Password": str(Password)})

            # add Job
            # scheduler.add_job("job1", update_regulary, 30)
            middleware.init_interval_job()

            return 'geht'

        return render_template('erpweclapp.html', form=form, name=name)

    if System == 'dynamics':
        form = erpformdynamics()
        col = db['Key_Dynamics']

        if form.validate_on_submit():

            BasicAuth = form.BasicAuth.data
            URL = form.URL.data

            datasets = col.insert_one(
                {"URL": str(URL), "BasicAuth": str(BasicAuth)})

            return 'geht'

        return render_template('erpdynamics.html', form=form, name=name)

    if System == 'xentral':
        form = erpformxentral()
        col = db['Key_Xentral']

        if form.validate_on_submit():
            Username = form.Username.data
            Password = form.Password.data
            URL = form.URL.data

            datasets = col.insert_one(
                {"URL": str(URL), "Username": str(Username), "Password": str(Password)})

            return 'geht'

        return render_template('erpxentral.html', form=form, name=name)

    if System == 'myfactory':
        form = erpformmyfactory()
        col = db['Key_MyFactory']

        if form.validate_on_submit():
            Username = form.Username.data
            Password = form.Password.data
            URL = form.URL.data

            datasets = col.insert_one(
                {"URL": str(URL), "Username": str(Username), "Password": str(Password)})

            return 'geht'

        return render_template('erpmyfactory.html', form=form, name=name)

    return 'geht nicht'


if __name__ == '__main__':
    app.run(debug=True)
