import xmltodict
from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth

app = Flask(__name__)




@app.route('/')
def homepage(): 
    url = "http://132.187.226.135/www/api//index.php/v1/artikel" 
    headers = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }

    response = requests.request("GET", url, auth=HTTPDigestAuth("Robin", "Robin")) #filtern nach "name_de oder "name_en"
    data = json.loads(response.text)
    return jsonify({"Result":data}) 

if __name__ == '__main__':
  app.run(debug=True)