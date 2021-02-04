import requests

url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"

payload={}
headers = {
  'AuthenticationToken': '22cca5be-4270-4f2d-9412-e7b582b4a85d',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)



#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
