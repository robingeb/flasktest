import requests

url = "http://10.105.11.42:7048/BC140/api/v1.0/items"   #"items" für die Artikelabfrage
                                                        #"?$filter=displayName eq 'Schutzblech vorn'" für bestimmten Artikel

payload={}
headers = {
  'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
