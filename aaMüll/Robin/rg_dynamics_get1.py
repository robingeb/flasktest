import requests
from requests.auth import HTTPBasicAuth

url = "http://10.105.11.42:7048/BC140/api/v1.0/items(19fde2b2-71c5-4e8f-954d-b6582169e6f1)/picture(19fde2b2-71c5-4e8f-954d-b6582169e6f1)"

payload = {}
auth=HTTPBasicAuth('wiinf\robin.gebhardt', 'UniWuerzburg2')

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
}

response = requests.request("GET", url, auth=auth headers=headers, #data=payload
)

print(response.text)