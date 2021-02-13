from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth

Datenstruktur = {
    "access":
    {   "release_to": "BDx2AOwdcfwBI9Grb52w"},
    "classification": 
        { "device_categorie_id": "AOoCdnoe1MXQ8Pa4AY7U" },
    "core": 
        {"articel_id_manufacturer": "Laurell Popp GmbH" ,
         "description_long": "Standard" ,
         "description_short": "Standard" ,
         "device_name": "Standard-Schlinge 1A" ,
         "keywords":  [
           { "0": "Schlinge"}  ],
         "manufacturer_id": "AR45f11oyyF5jUxC9FfH" },
    "historical_data":
        {"created_at": "16. Dezember 2020 um 10:41:33 UTC+1" ,
         "created_by": "HKyUyCuVj0g12htOsAPmGCcffBq2" ,
         "updated_at": "16. Dezember 2020 um 10:41:33 UTC+1" ,
         "updated_by": "HKyUyCuVj0g12htOsAPmGCcffBq2" },
    "media":
        {"attachments":  [
            { "device_image": "https://firebasestorage.googleapis.com/v0/b/tagideasy.appspot.com/o/devices%2F05Uh1VJktu4RaquIgPnh%2Fmedia%2Fdevice_image?alt=media&token=032fd1db-a1b3-484f-8091-9af4a4e82f32"}  
            ]}
}
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def get_weclapp():

    url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    headers = {
    'AuthenticationToken': '8e98b02b-eb0e-4ea8-a443-9d8dcada588f'
    }
    
    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    #res = {} 
    #for key, value in data.items(): 
        #res[int(key)] = [int(item) for item in value]
    #data["device_name"] = data["name"] #prints 1,2,3...Device Data
    #del data["name"]

    # for i in list(data): 
    #     if i == data["result"][0]["name"]:
    #         data["device_name"] = data["result"][0]["name"]
    #         del data["result"][0]["name"]
            #data["device_name1"] = data["result"][1]["name"]
            #data["device_name2"] = data["result"][2]["name"]
    #del data["result"][0]["name"]
    #del data["result"][1]["name"]

    # class person(object):
    #     def __init__(self,name):
    #         self.name = name
    # alternate = {person("device_name"): data["result"][0]["name"]}

    # alternate[data["device_name"]] = data["result"][0]["name"] 

    # del data["result"][0]["name"]
    # data["device_name"] = data["result"][1]["name"]
    # del data["result"][1]["name"]

    #return(jsonify({"Ergebnis": data}))

    data["result"][0]["device_name"] = data["result"][0]["name"]
    # del data["result"][0]["name"]
    # data["result"][1]["device_name"] = data["result"][1]["name"]
    # del data["result"][1]["name"]
    # data["result"][2]["device_name"] = data["result"][2]["name"]
    # del data["result"][2]["name"]
    # data["result"][3]["device_name"] = data["result"][3]["name"]
    # del data["result"][3]["name"]
    # data["result"][4]["device_name"] = data["result"][4]["name"]
    # del data["result"][4]["name"]
    # data["result"][5]["device_name"] = data["result"][5]["name"]
    # del data["result"][5]["name"]
    # data["result"][6]["device_name"] = data["result"][6]["name"]
    # del data["result"][6]["name"]
    # data["result"][7]["device_name"] = data["result"][7]["name"]
    # del data["result"][7]["name"]
    # data["result"][8]["device_name"] = data["result"][8]["name"]
    # del data["result"][8]["name"]
    # data["result"][9]["device_name"] = data["result"][9]["name"]
    # del data["result"][9]["name"]
    # data["result"][10]["device_name"] = data["result"][10]["name"]
    # del data["result"][10]["name"]
    # data["result"][11]["device_name"] = data["result"][11]["name"]
    # del data["result"][11]["name"]
    # data["result"][12]["device_name"] = data["result"][12]["name"]
    # del data["result"][12]["name"]
    # data["result"][13]["device_name"] = data["result"][13]["name"]
    # del data["result"][13]["name"]
    # data["result"][14]["device_name"] = data["result"][14]["name"]
    # del data["result"][14]["name"]
    #i = list(range(1,15))
    for d in data.items():
        for i in list(range(1,15)):
            if d == data["result"][i]["name"]:
                data["result"][i]["device_name"] = data["result"][i]["name"]
    return (jsonify({"Ergebnis": data}))

    
    
    
    
    #return(jsonify({"Ergebnis": data}))



if __name__ == "__main__":
    app.run(port=1337, debug=True)