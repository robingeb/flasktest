from flask import Flask, request, make_response, jsonify, json
import requests


#Erstellt neue Apllikationi
app = Flask(__name__)

@app.route('/')
def homepage(): 
    url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    #payload = {}
    headers = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }

    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    #Filtert und sortiert Daten
    article = [data["result"][x]["id"] for x in range(len(data["result"]))]
    #ARG = data (ohne filter)
    return jsonify(article)  


if __name__ == '__main__':
  app.run(debug=True)