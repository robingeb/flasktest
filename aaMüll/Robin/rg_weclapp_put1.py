import requests

url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"

payload=" {\r\n            \r\n            \"active\": false,\r\n       \"applyCashDiscount\": true,\r\n            \"articleNumber\": \"002\",\r\n            \"availableInSale\": true,\r\n            \"availableInShop\": false,\r\n            \"batchNumberRequired\": false,\r\n            \"billOfMaterialPartDeliveryPossible\": false,\r\n            \"name\": \"Fahrradreifen\",\r\n            \"productionArticle\": false,\r\n            \"serialNumberRequired\": false,\r\n            \"showOnDeliveryNote\": true,\r\n            \"taxRateType\": \"STANDARD\",\r\n            \"unitId\": \"2895\",\r\n            \"unitName\": \"Stk.\",\r\n            \"useSalesBillOfMaterialItemPrices\": false,\r\n            \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n        }"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'AuthenticationToken': '22cca5be-4270-4f2d-9412-e7b582b4a85d',
  'Cookie': '_sid_=1'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
print('hi')