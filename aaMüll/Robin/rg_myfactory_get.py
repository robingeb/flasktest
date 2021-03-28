import requests

url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel/"
auth = {
  'username': 'HB',
  "password": "HB"
}
   
response = requests.request("GET", url, auth=(auth['username'], auth['password']))    
response = response.text
print(response)

