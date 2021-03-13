from flask import Flask, request, make_response, jsonify, json
import requests




def start(): 
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items" #?$filter=displayName eq 'Schutzblech vorn'"
    #payload = {}
    auth = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }

    # response = requests.request("GET", url, headers=headers) #data = payload
    # data = json.loads(response.text)
    #Filtert und sortiert Daten
    #for displayName in data:
        #   return(displayName)
    #return(response.text)
    dynamicsAPI = DynamicsAPI(url, auth)
    data = dynamicsAPI.get_request()
    print(data)




class DynamicsAPI():
    def __init__(self, url, auth):       
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