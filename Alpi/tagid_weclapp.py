import requests
import json
from requests.auth import HTTPDigestAuth


url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
headers = {
    'AuthenticationToken': '8e98b02b-eb0e-4ea8-a443-9d8dcada588f'
}
    
response = requests.request("GET", url, headers=headers) #data = payload
data = json.loads(response.text)
#res = {} 
#for key, value in data.items(): 
#res[int(key)] = [int(item) for item in value]
#prints 1,2,3...Device Data
#del data["name"]
#for key in data:
#data.update({"name": "device"})   
#keys_values = data.items()
#new_d = {str(key): str(value) for key, value in keys_values}
#new_d["device_name"] = new_d["name"]
#del new_d["name"]
data["result"][0]["device_name"] = data["result"][0]["name"]

#del data["result"][0]["name"]
for key, value in data.items() :
    print(key, value)
    
i = list(range(1,15))
print(i)
    
#data["result"][2]["name"] !!!
#print(({"Ergebnis": new_dict}))