from flask import Flask, render_template, url_for, render_template, request, redirect
from rg_forms import NameForm, articleForm, choiceform, erpformweclapp, erpformdynamics, erpformmyfactory, erpformxentral
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__,template_folder = 'templates')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True

app.config["MONGO_URI"] = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
mongo = PyMongo(app)
client = pymongo.MongoClient("mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test")






@app.route('/choice', methods=['GET', 'POST'])
def choice():
    name = None
    form = choiceform()
  
    if form.validate_on_submit():
        System = str(form.System.data)
        
        return redirect(url_for('erp', System = System))
   
    
    return render_template('choice.html', form=form, name=name)


@app.route('/erp/<string:System>', methods=['GET', 'POST'])
def erp(System):
    name = None
    db = client['Keys']
    



    if System == 'weclapp':
        form = erpformweclapp()
        col = db['Key_Weclapp']
       

        if form.validate_on_submit():
            URL = form.URL.data
            Password = form.Password.data
            
            datasets = col.insert_one({"URL": str(URL), "Password": str(Password)})

        
            return 'geht'

        return render_template('erpweclapp.html', form=form, name=name)


    if System == 'dynamics':
        form = erpformdynamics()

        if form.validate_on_submit():
            Username = form.Username.data
            Password = form.Password.data
            zugangsdaten = str(Username) + "," + str(Password)

        
            return redirect(url_for('index', zugangsdaten = zugangsdaten))

        return render_template('erpdynamics.html', form=form, name=name)
    


    if System == 'xentral':
        form = erpformxentral()

        if form.validate_on_submit():
            URL = form.URL.data
            Password = form.Password.data
            zugangsdaten = str(URL) + "," + str(Password)

        
            return redirect(url_for('index', zugangsdaten = zugangsdaten))

        return render_template('erpxentral.html', form=form, name=name)


    if System == 'myfactory':
        form = erpformmyfactory()

        if form.validate_on_submit():
            URL = form.URL.data
            Password = form.Password.data
            

            
           
            

        
            return 'geht'

        return render_template('erpmyfactory.html', form=form, name=name)
    
    return 'geht nicht'







if __name__ == '__main__':
    app.run(debug=True)


