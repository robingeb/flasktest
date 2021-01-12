from flask import Flask, request
import requests



url = "https://gebhardt.weclapp.com/webapp/api/v1/contact?page=1&pageSize=100&sort="
headers = {
  'AuthenticationToken': '8c0fb5fb-ece8-4878-a9a8-f54b0d623fa7',
}

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/test')
def json():
    payload={}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

if __name__ == '__main__':
    app.run(debug=True)









