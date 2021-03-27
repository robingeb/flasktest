
#https://docs.microsoft.com/de-de/dynamics-nav/api-reference/v1.0/api/dynamics_create_item

import requests
from requests.auth import HTTPBasicAuth

url = "http://10.105.11.42:7048/BC140/api/beta/items(52c3bc8b-77b1-4f31-99a0-00060298517c)/picture(52c3bc8b-77b1-4f31-99a0-00060298517c)/content"


#3 Entitäten müssen aus der Standarddatei entfernt werden, taxgroup, item Category, base Unit of Measure

#payload= "{\r\n  \"number\": \"102robin\",\r\n  \"displayName\": \"ATHENS Desk\",\r\n  \"type\": \"Inventory\",\r\n  \"blocked\": false,\r\n  \"gtin\": \"\",\r\n  \"inventory\": 0,\r\n  \"unitPrice\": 1000.8,\r\n  \"priceIncludesTax\": false,\r\n  \"unitCost\": 780.7\r\n} "


auth=HTTPBasicAuth('wiinf\robin.gebhardt', 'UniWuerzburg2')

headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, auth=auth)

print(response.text)
