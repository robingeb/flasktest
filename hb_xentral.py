import xmltodict
#from flask import jsonify
import requests
import json

def start():
    url = "http://132.187.226.135/api/v1/artikel"
    auth = {
    'username': 'HB',
    "password": "HB"
    }
    xentralApi = XentralAPI(url, auth)
    xentralApi.get_request()


class XentralAPI():
    def __init__(self, url, auth):        
        self.url = url
        self.auth = auth

   


    def get_request(self):
        response = requests.request("GET", self.url, auth=(self.auth['username'], self.auth['password']))
        data = json.loads(response.text)
        #Filtert und sortiert Daten
        # article = [data["result"][x]["name"] for x in range(len(data["result"]))]
        #ARG = data (ohne filter)
        #return jsonify(article)
        print(data) 
        

        
    def post_request(self):
        pass
        

    def delete_request(self):
        pass


if __name__ == "__main__":
    start()

    