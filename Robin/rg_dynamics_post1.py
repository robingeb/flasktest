
#https://docs.microsoft.com/de-de/dynamics-nav/api-reference/v1.0/api/dynamics_create_item

import requests

url = "http://10.105.11.42:7048/BC140/api/beta/items(52c3bc8b-77b1-4f31-99a0-00060298517c)/picture(52c3bc8b-77b1-4f31-99a0-00060298517c)/content"


#3 Entitäten müssen aus der Standarddatei entfernt werden, taxgroup, item Category, base Unit of Measure

#payload= "{\r\n  \"number\": \"102robin\",\r\n  \"displayName\": \"ATHENS Desk\",\r\n  \"type\": \"Inventory\",\r\n  \"blocked\": false,\r\n  \"gtin\": \"\",\r\n  \"inventory\": 0,\r\n  \"unitPrice\": 1000.8,\r\n  \"priceIncludesTax\": false,\r\n  \"unitCost\": 780.7\r\n} "
# {
#   "number": "1896-S",
#   "displayName": "ATHENS Desk",
#   "type": "Inventory",adsfd
#   "blocked": false,
#   "gtin": "",
#   "inventory": 0,
#   "unitPrice": 1000.8,
#   "priceIncludesTax": false,
#   "unitCost": 780.7
# } 
headers = {
  'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0=',
  'Content-Type': 'application/octet-stream',
  'If-Match': W/"'JzQ0O0txVU5qdldENWxnK3BrcDI5UFNueE5OTVAwVno3T01kVzBBZG9OZjQ5RzQ9MTswMDsn'"
}

response = requests.request("PATCH", url, headers=headers)

print(response.text)
