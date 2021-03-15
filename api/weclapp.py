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
    #payload="{\r\n    \"id\": \"3814\",\r\n    \"active\": true,\r\n    \"articleNumber\": \"012\",\r\n    \"applyCashDiscount\": true,\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"productionArticle\": false,\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useAvailableForSalesChannels\": false,\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false,\r\n\t\"name\": \"Fahrradsitz Neu Neu Neu\"\r\n}"

    payload = """{
        "id": "3814",
        "active": true,
        "articleNumber": "012",
        "applyCashDiscount": true,
        "availableInSale": true,
        "availableInShop": false,
        "batchNumberRequired": false,
        "billOfMaterialPartDeliveryPossible": false,
        "productionArticle": false,
        "serialNumberRequired": false,
        "showOnDeliveryNote": true,
        "taxRateType": "STANDARD",
        "unitId": "2895",
        "unitName": "Stk.",
        "useAvailableForSalesChannels": false,
        "useSalesBillOfMaterialItemPrices": false,
        "useSalesBillOfMaterialItemPricesForPurchase": false,
        "name": "Fahrradsitz Neu2"
    }"""

    weClappAPI = WeClappAPI(url, auth)
    weClappAPI.put_request(payload, 3814)


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
        response = requests.request("GET", self.url, headers=self.auth)
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
        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response.text

    def put_request(self, payload, id):
        """
        Führt einen PUT-Request durch.

        :param payload: als json formatierter string mit aktualisierter Instanz.
        :param id: id der Instanz in WeClapp.
        :return: ein Dictionary mit Instanz, welche durch den Request verändert wurd.
        """  
        print("test_put_request")
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        response = requests.request("PUT", self.url + "/id/" +str(id), headers=headers, data=payload)
        return response.text

if __name__ == "__main__":
    test()