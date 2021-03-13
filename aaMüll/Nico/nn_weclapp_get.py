
import requests

url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"

payload={}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'AuthenticationToken': '1e249f3c-6c3b-42cf-96ba-313dd93d1ddf',
  'Cookie': 'JSESSIONID=FL5V8hjFUnDLrrPC6hbvaSkjU9O3t4E-URyDVDXV.app; _sid_=1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
