from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth


app = Flask(__name__)

@app.route('/')
def homepage(): 
    url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"

    
    response = requests.request("GET", url, auth="Alperen.Yildirim@stud-mail.uni-wuerzburg.de") 
    data = json.loads(response.text)
    return jsonify(data)  


if __name__ == '__main__':
  app.run(debug=True)