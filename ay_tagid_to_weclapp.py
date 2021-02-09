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
    output = []
    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    #data["device_name"] = data["result"][0] #prints 1,2,3...Device Data
    data["device_name"] = data["result"][0]
    del data["result"]
    #print(data)
    for key in data:
        return(jsonify({"Ergebnis": data}))


if __name__ == "__main__":
    app.run(port=1337, debug=True)