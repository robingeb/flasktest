from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth

app = Flask(__name__)




@app.route('/', methods=["GET", "POST"])
def homepage(): 
    url = "http://132.187.226.135/www/api//index.php/v1/artikel" 
    auth = {
    'username': 'Alpi',
    "password": "Alpi"
    }
    if request.method == "GET":
      response = requests.request("GET", url, auth=HTTPDigestAuth(auth['username'], auth['password'])) #filtern nach "name_de" oder "name_en"
      data = json.loads(response.text)
      return jsonify({"Result":data}) 
    elif request.method == "POST":
      headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': '_sid_=1'
            }
      response = requests.request("POST", url, auth=HTTPDigestAuth(auth['username'], auth['password'], data=payload)) 
      data = json.loads(response.text)
      return jsonify({"Result":data})


  
if __name__ == '__main__':
  app.run(debug=True)