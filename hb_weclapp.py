import xmltodict
#from flask import jsonify
import requests
import json
from requests.auth import HTTPDigestAuth


def start():
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }
    weClappAPI = WeClappAPI(url, auth)
    # Um verschiedene Methoden (get, post, delete) zu starten, hier entsprechnde Methode wählen
    weClappAPI.get_request()
    #weClappAPI.post_request(payload)


class WeClappAPI():
    def __init__(self, url, auth, payload = None):        
        self.url = url
        self.auth = auth
        self.payload = payload

   


    def get_request(self):
        response = requests.request("GET", self.url, headers=self.auth)
        data = json.loads(response.text)
        #Filtert und sortiert Daten
        article = [data["result"][x]["name"] for x in range(len(data["result"]))]
        #ARG = data (ohne filter)
        #return jsonify(article)
        print(article) 
        

        
    def post_request(self, payload):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        print(response.text)
        

    def delete_request(self):
        pass

if __name__ == "__main__":
    start()