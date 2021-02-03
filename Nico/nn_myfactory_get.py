import requests

url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"

payload={}
headers = {
  'Authorization': 'Basic VGVzdDoxMjM0'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
