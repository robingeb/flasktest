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
    # Um verschiedene Methoden (get, post, delete) zu starten, hier entsprechnde Methode wählen
    #weClappAPI.get_request()
    #weClappAPI.post_request(payload)
    weClappAPI.put_request(payload, 3814)


class WeClappAPI():
    def __init__(self, url, auth):
        """
        Zugriff auf die WeClapp-API
        param: 
        url: Url des zu verknüpfenden Systems
        auth: Authentfizierungstoken
        """        
        self.url = url
        self.auth = auth
        #self.payload = payload

   


    def get_request(self):
        response = requests.request("GET", self.url, headers=self.auth)
        data = json.loads(response.text)
        #Filtert und sortiert Daten
        #article = [data["result"][x]["id"] for x in range(len(data["result"]))]
        #ARG = data (ohne filter)
        #return jsonify(article)
        return data 
        

        
    def post_request(self, payload):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response.text

    def put_request(self, payload, id):
        print("test_put_request")
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'AuthenticationToken': self.auth["AuthenticationToken"],
            'Cookie': '_sid_=1'
        }
        response = requests.request("PUT", self.url + "/id/" +str(id), headers=headers, data=payload)
        return response.text
        

    # def delete_request(self, id):
    #     response = requests.request("DELETE", self.url + "/" + id, headers=headers)
    #     return(response)

if __name__ == "__main__":
    start()