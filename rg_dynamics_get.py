import requests

url = "http://10.105.11.42:7048/BC140/api/v1.0/vendors"

#payload=" {\r\n            \"id\": \"3396\",\r\n            \"version\": \"0\",\r\n            \"active\": true,\r\n            \"applyCashDiscount\": true,\r\n            \"articleAlternativeQuantities\": [],\r\n            \"articleImages\": [],\r\n            \"articleNumber\": \"006\",\r\n            \"articlePrices\": [],\r\n            \"articleType\": \"STORABLE\",\r\n            \"availableForSalesChannels\": [],\r\n            \"availableInSale\": true,\r\n            \"availableInShop\": false,\r\n            \"batchNumberRequired\": false,\r\n            \"billOfMaterialPartDeliveryPossible\": false,\r\n            \"createdDate\": 1610556205767,\r\n            \"customAttributes\": [],\r\n            \"defaultWarehouseLevels\": [],\r\n            \"description\": \"<p>Erstellt zum Testen der eines Api zugriffs</p>\",\r\n            \"lastModifiedDate\": 1610556205766,\r\n            \"marginCalculationPriceType\": \"PURCHASE_PRICE_PRODUCTION_COST\",\r\n            \"name\": \"Fahrradpedal\",\r\n            \"productionArticle\": false,\r\n            \"productionBillOfMaterialItems\": [],\r\n            \"salesBillOfMaterialItems\": [],\r\n            \"serialNumberRequired\": false,\r\n            \"showOnDeliveryNote\": true,\r\n            \"supplySources\": [],\r\n            \"tags\": [],\r\n            \"taxRateType\": \"STANDARD\",\r\n            \"unitId\": \"2895\",\r\n            \"unitName\": \"Stk.\",\r\n            \"useAvailableForSalesChannels\": false,\r\n            \"useSalesBillOfMaterialItemPrices\": false,\r\n            \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n        }"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Basic V0lJTkZccm9iaW4uZ2ViaGFyZHQ6a2lCVEVLTnFaVzYyN24zQXl1TkQ0YzJFdVpwQkZJM3dLZE9OcXlaa2JXbz0='
}

response = requests.request("GET", url, headers=headers, #data=payload
)

print(response.text)