import xmltodict
#from flask import jsonify
import requests
import json
from requests.auth import HTTPDigestAuth

#TODO: ERROR für fehlerhafte Internetverbindung, fehlerhafter Zugriff auf API

def test():    
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }
    payload = '{\n    "name": "Hebebuehne",\n    "unitId": 2895\n, "articleNumber":1 \n}'

    weClappAPI = WeClappAPI(url, auth)
    print(weClappAPI.post_request(payload))


class WeClappAPI():
    """
    Zugriff auf die Api von WeClapp. 

    :param str url: gültige Zugangsurl zu Dynamics.
    :param dict auth: Authentifizierungsdaten Form: {"AuthenticationToken": string } 
    """

    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
   
    def get_request(self):
        """
        Führt einen GET-Request durch.

        :return: ein Dictionary mit Ergebniss des Requests.
        """  
        try:
            response = requests.request("GET", self.url, headers=self.auth)
        except:
            raise Exception(
                "Connection Failed \n Überprüfe: \n fehlerhafte URL oder Authentifizerungsdaten")
        data = json.loads(response.text)
        return data 
              
    def post_request(self, payload):
        """
        Führt einen POST-Request durch.

        :param json payload:  als json formatierter string mit zur hinzufügenden Instanz.  
        :return: ein Dictionary mit Instanz, welche nach Dynamics geladen wurden.
        """  
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        try: 
            response = requests.request("POST", self.url, headers=headers, data=payload)
        except:
            raise Exception(
                "Connection Failed \n Überprüfe: \n fehlerhafte URL oder Authentifizerungsdaten")
        return response.text

    def put_request(self, payload, id):
        """
        Führt einen PUT-Request durch.

        :param payload: als json formatierter string mit aktualisierter Instanz.
        :param id: id der Instanz in WeClapp.
        :return: ein Dictionary mit Instanz, welche durch den Request verändert wurd.
        """  
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        try:
            response = requests.request("PUT", self.url + "/id/" +str(id), headers=headers, data=payload)
        except:
            raise Exception(
                "Connection Failed \n Überprüfe: \n fehlerhafte URL oder Authentifizerungsdaten")
        return response.text

if __name__ == "__main__":
    test()