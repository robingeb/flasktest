
import requests
import json
from requests.auth import HTTPDigestAuth


url = " http://132.187.226.135/www/api//index.php/v1/artikel"


response = requests.request("GET", url, auth=HTTPDigestAuth("Robin", "Robin"))
data = json.loads(response.text)
print(data) 
print('hi')
        
        