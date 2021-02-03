from flask import Flask, request, make_response, jsonify, json
import requests
import json
from requests.auth import HTTPDigestAuth



app = Flask(__name__)

@app.route('/')
def homepage(): 
    url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    headers = {
    'AuthenticationToken': '8e98b02b-eb0e-4ea8-a443-9d8dcada588f'
    }

    response = requests.request("GET", url, headers=headers) #data = payload
    data = json.loads(response.text)
    return jsonify(data)  


if __name__ == '__main__':
  app.run(debug=True)




