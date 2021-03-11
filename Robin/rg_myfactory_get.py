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
    print(response)
    


if __name__ == "__main__":
    get_request()