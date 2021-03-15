from flask import Flask, request, make_response, jsonify, json
import requests


def test(): 
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items" 
    auth = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }
    dynamicsAPI = DynamicsAPI(url, auth)
    data = dynamicsAPI.get_request()
    print(data)


class DynamicsAPI():
    """
    Zugriff auf die Api von Dynamics. 

    :param str url: gültige Zugangsurl zu Dynamics
    :param dict auth: Authentifizierungsdaten Form: {"Authorization": string } 
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
        :return: ein Dictionary mit Instanz, welche nach Dynamics geladen wurde.
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
        :param id: id der Instanz in Dynamics.
        :return: ein Dictionary mit Instanz, welche durch den Request verändert wurde.
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