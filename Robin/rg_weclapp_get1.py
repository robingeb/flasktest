import requests

url = "https://gebhardt.weclapp.com/webapp/api/v1/contact?page=1&pageSize=100&sort="

payload={}
headers = {
  'AuthenticationToken': '8c0fb5fb-ece8-4878-a9a8-f54b0d623fa7',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)



#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
