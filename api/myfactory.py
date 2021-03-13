import requests
import xmltodict
from flask import jsonify

url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"
auth = {
  'username': 'HB',
  "password": "HB"
}


def get_request():
    
    response = requests.request("GET", url, auth=(auth['username'], auth['password']))    
    content_dict = xmltodict.parse(response.text)
    #return jsonify(content_dict)
    print(content_dict)
    
def post_request():
    """Post ist leider nicht möglich. Nur lesender Zugriff über API erlaubt. Alternative: Datenimport von MyFactory. 
    Daten werden von unserem Tool in das benötigten Format transformiert und können dann händisch importiert werden """
    #response = requests.request("POST", url, auth=(auth['username'], auth['password']), data=payload)
    #print(response.text)
    pass
    

def delete_request():
    """Delete-Request ebenfalls nicht möglich"""
    pass


if __name__ == "__main__":
    get_request()