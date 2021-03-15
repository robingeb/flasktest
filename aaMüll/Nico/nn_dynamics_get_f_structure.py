
from flask import Flask, request, make_response, jsonify, json
import requests


#Erstellt neue Apllikationi
app = Flask(__name__)

@app.route('/')
def homepage(): 
    url = "http://10.105.11.42:7048/BC140/api/v1.0/items"
    #payload = {}
    headers = {
    'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
    }

    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    #Filtert und sortiert Daten
   
def filter_set(data, search_string):
    def iterator_func(x):
        for v in x.values():
            if search_string in v:
                return True
            return False
        return filter(iterator_func, data)
  
    filtered_records = filter_set(data, "displayName")

    return jsonify(list(filtered_records))

if __name__ == '__main__':
  app.run(debug=True)

