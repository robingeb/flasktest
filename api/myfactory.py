import requests
import xmltodict
from flask import jsonify


def test(): 
    url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"
    auth = {
    'username': 'HB',
    "password": "HB"
    }
    myFactoryAPI = MyFactoryAPI(url,auth)
    print(myFactoryAPI.get_request())


class MyFactoryAPI():
    """
        Zugriff auf die Api von MyFactory

        :param str url: gültige Zugangsurl zu MyFactory
        :param dict auth: Authentifizierungsdaten Form: {"username": name, "password": password } 
    """

    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def get_request(self):
        """
        Führt einen get-Request durch.

        :return: ein Dictionary mit Ergebniss des Requests.
        """        
        response = requests.request("GET", self.url, auth=(self.auth['username'], self.auth['password']))    
        content_dict = xmltodict.parse(response.text)        
        return content_dict
        
    def post_request(self):
        """Post ist nicht möglich. Nur lesender Zugriff über API erlaubt. Alternative: Datenimport von MyFactory. 
        Daten werden von unserem Tool in das benötigten Format transformiert und können dann händisch importiert werden """
        #response = requests.request("POST", url, auth=(auth['username'], auth['password']), data=payload)
        #print(response.text)
        pass
        

    def delete_request(self):
        """Delete-Request ebenfalls nicht möglich"""
        pass


if __name__ == "__main__":
    test()