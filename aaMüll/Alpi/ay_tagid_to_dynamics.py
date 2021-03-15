from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth


app = Flask(__name__)



@app.route('/')
def homepage(): 
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items" #?$filter=displayName eq 'Schutzblech vorn'"
    #payload = {}
    headers = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }

    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    #Filtert und sortiert Daten
    #for displayName in data:
     #   return(displayName)
    #return(response.text)

    data["value"][0]["device_name"] = data["value"][0]["displayName"]
    del data["value"][0]["displayName"]
    data["value"][1]["device_name"] = data["value"][1]["displayName"]
    del data["value"][1]["displayName"]
    data["value"][2]["device_name"] = data["value"][2]["displayName"]
    del data["value"][2]["displayName"]
    data["value"][3]["device_name"] = data["value"][3]["displayName"]
    del data["value"][3]["displayName"]
    data["value"][4]["device_name"] = data["value"][4]["displayName"]
    del data["value"][4]["displayName"]
    data["value"][5]["device_name"] = data["value"][5]["displayName"]
    del data["value"][5]["displayName"]
    data["value"][6]["device_name"] = data["value"][6]["displayName"]
    del data["value"][6]["displayName"]
    data["value"][7]["device_name"] = data["value"][7]["displayName"]
    del data["value"][7]["displayName"]
    data["value"][8]["device_name"] = data["value"][8]["displayName"]
    del data["value"][8]["displayName"]
    data["value"][9]["device_name"] = data["value"][9]["displayName"]
    del data["value"][9]["displayName"]
    data["value"][10]["device_name"] = data["value"][10]["displayName"]
    del data["value"][10]["displayName"]
    data["value"][11]["device_name"] = data["value"][11]["displayName"]
    del data["value"][11]["displayName"]
    data["value"][12]["device_name"] = data["value"][12]["displayName"]
    del data["value"][12]["displayName"]
    data["value"][13]["device_name"] = data["value"][13]["displayName"]
    del data["value"][13]["displayName"]
    data["value"][14]["device_name"] = data["value"][14]["displayName"]
    del data["value"][14]["displayName"]

    data["value"][0]["serial number"] = data["value"][0]["number"]
    del data["value"][0]["number"]
    data["value"][1]["serial number"] = data["value"][1]["number"]
    del data["value"][1]["number"]
    data["value"][2]["serial number"] = data["value"][2]["number"]
    del data["value"][2]["number"]
    data["value"][3]["serial number"] = data["value"][3]["number"]
    del data["value"][3]["number"]
    data["value"][4]["serial number"] = data["value"][4]["number"]
    del data["value"][4]["number"]
    data["value"][5]["serial number"] = data["value"][5]["number"]
    del data["value"][5]["number"]
    data["value"][6]["serial number"] = data["value"][6]["number"]
    del data["value"][6]["number"]
    data["value"][7]["serial number"] = data["value"][7]["number"]
    del data["value"][7]["number"]
    data["value"][8]["serial number"] = data["value"][8]["number"]
    del data["value"][8]["number"]
    data["value"][9]["serial number"] = data["value"][9]["number"]
    del data["value"][9]["number"]
    data["value"][10]["serial number"] = data["value"][10]["number"]
    del data["value"][10]["number"]
    data["value"][11]["serial number"] = data["value"][11]["number"]
    del data["value"][11]["number"]
    data["value"][12]["serial number"] = data["value"][12]["number"]
    del data["value"][12]["number"]
    data["value"][13]["serial number"] = data["value"][13]["number"]
    del data["value"][13]["number"]
    data["value"][14]["serial number"] = data["value"][14]["number"]
    del data["value"][14]["number"]
    for keys in data.keys():
        print(keys)

    return jsonify({"Result":data})



if __name__ == "__main__":
    app.run(port=1337, debug=True)