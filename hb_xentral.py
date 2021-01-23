import xmltodict
#from flask import jsonify
import requests
import json

#TODO: API Zugriff auf Xentral funktioniert nicht (404 Not Fount Error)

def start():
    url = "http://132.187.226.135/api/v1/artikel"
    auth = {
    'username': 'HB',
    "password": "HB"
    }
    xentralApi = XentralAPI(url, auth)
    xentralApi.get_request()


class XentralAPI():
    def __init__(self, url, auth, payload = None):        
        self.url = url
        self.auth = auth
        self.payload = payload

   


    def get_request(self):
        response = requests.request("GET", self.url, auth=(self.auth['username'], self.auth['password']))
        data = json.loads(response.text)
        #Filtert und sortiert Daten
        # article = [data["result"][x]["name"] for x in range(len(data["result"]))]
        #ARG = data (ohne filter)
        #return jsonify(article)
        print(data) 
        

        
    def post_request(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
             #'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43',
            'Cookie': '_sid_=1'
            }
        response = requests.request("POST", self.url, auth=(self.auth['username'], self.auth['password']), data=self.payload)
        print(response.text)
        

    def delete_request(self):
        pass


if __name__ == "__main__":
    start()

    