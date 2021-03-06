try:
    from flask import Flask, json, jsonify, make_response, request, Response, render_template
    import requests
    from http import HTTPStatus
    from flask_pymongo import PyMongo
    import pymongo
    from pymongo import MongoClient
    import datetime
    import json
    from bson import ObjectId
    from bson.json_util import loads
    import pandas as pd
  
    print("All Modules are loaded")

except Exception as e:
    print("Some Modules are missing {}".format(e))

app = Flask(__name__)


#app.config["MONGO-URI"] = "URI"
#mongo = PyMongo(app)
#client = pymongo.MongoClient(URI)
#pymongo.decending 
#mehrere db & collections können über eine Request in einer URL abgefragt werden
#find() + limit um Response auf ein Paar Output-Elemente zu reduzieren

app.config["MONGO_URI"] = "mongodb+srv://USER1:mamu13@cluster0.loonh.mongodb.net/test?authSource=admin&replicaSet=atlas-n1o4yx-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
mongo = PyMongo(app)
client = pymongo.MongoClient("mongodb+srv://USER1:mamu13@cluster0.loonh.mongodb.net/test?authSource=admin&replicaSet=atlas-n1o4yx-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

    

#@app.route("/html", methods = ["GET"])
#def html():
    #return render_template('blog.html')

#def parse_json(data):
   #return json.loads(json_util.dumps(data))


@app.route("/")
def sayHitoPJS():
    return "Hi Guys"

@app.route("/Stammdaten1", methods = ["GET"])
def Stammdaten_A():
    
        db = client["Prüfdaten"]
        Stammdaten = db["Unternehmen_1"].find({})

        for q in Stammdaten:    
            x = print(q["ger"])
        return jsonify({"Result":x})
                
         

#keyerror vermeiden: value = mydict.get(key, default_value)
#CSV Dateien abfragen nach bestimmten Parametern
@app.route("/Stammdaten", methods = ["GET"])
def Stammdaten_Abfrage():
    try:
        db = client["Prüfdaten"]
        Stammdaten = db["Unternehmen_1"].find({})

        output = []

        for q in Stammdaten:    
                output.append({
                    "ger": q["ger"],
                    "pruefer": q["pruefer"],
                    "prueftag": q["prueftag"],
                    "pnext": q["pnext"],
                    "created_at": q["created_at"],
                    "bgv": q["bgv"],
                    "ergebnis": q["ergebnis"],
                    "bemerkung": q["bemerkung"]
                })
        if output:
            return jsonify({"Result": output}), HTTPStatus.OK #this or return jsonify({"Result": output, "status": "ok"}, 200)
        elif not output:
            return jsonify({"Message": "Non-existing Product-Name inserted",
                            "Detail": "Check your input and correct Product-Name"}), HTTPStatus.NOT_FOUND 
    except pymongo.errors.ConnectionFailure: #or KeyError:
        #value = default_value
        return HTTPStatus.NOT_FOUND

#double for loop for q in Stammdaten:
            #output.append({
             #   "ger": q["ger"],
            #})
            #for y in output:
             #   list.append({
             #       "hersteller": q["hersteller"]
              #  }) --> if need specific data in "ger"
#<param> string, <int:param> integer
#eine bestimmte Datei/Unternehmen abfragen
@app.route("/Abfragen/Stammdaten/<hersteller>", methods = ["GET"])      #, "POST", "PUT", "DELETE"
def Artikel_Abfrage_Anlage(hersteller):
    try:
        db = client["Prüfdaten"]
        Stammdaten = db["Unternehmen_1"].find({"ger.hersteller": hersteller})
        

        output = []
        

        for q in Stammdaten:
            output.append({
                "ger": q["ger"]
            })
        if output:
            return jsonify({"Hersteller": hersteller}, {"Result": output}), HTTPStatus.OK #this or
        elif not output:
            return jsonify({"Message": "Non-existing Product-Name inserted",
                            "Detail": "Check your input and correct Product-Name"}), HTTPStatus.NOT_FOUND 
    
    except pymongo.errors.ConnectionFailure:
        return HTTPStatus.NOT_FOUND




@app.route("/Anlegen/Stammdaten/<hersteller>", methods = ["GET", "POST"])
def neuesPrüfzeugnis(hersteller):
    try:
        db = client["Prüfdaten"]
        Stammdaten = db["Unternehmen_1"].insert_one({"hersteller": hersteller})

        output = []
        
        if request.method == "POST":  
            for q in Stammdaten:
                output.append({
                    "ger": q["ger"]
                })
        return jsonify({"Result": output})
    except pymongo.errors.ConnectionFailure:
        return HTTPStatus.NOT_FOUND

# VERGLEICHEN

@app.route('/test')
def homepage(): 
    url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    #payload = {}
    headers = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }

    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    article = [data["result"][x]["name"] for x in range(len(data["result"]))]
    return jsonify(article)   
    
    
if __name__ == '__main__':
  app.run(debug=True)







if __name__ == "__main__":
    app.run(port = 1337, debug = True)