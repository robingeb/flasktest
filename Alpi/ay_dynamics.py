from flask import Flask, request, make_response, jsonify, json
import requests


#Erstellt neue Apllikationi
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
    return jsonify({"Result":data})


# class DynamicsAPI():
#     def __init__(self, url, auth):
#         """
#         Zugriff auf die WeClapp-API
#         param: 
#         url: Url des zu verknüpfenden Systems
#         auth: Authentfizierungstoken
#         """        
#         self.url = url
#         self.auth = auth
#         #self.payload = payload


if __name__ == '__main__':
  app.run(debug=True)