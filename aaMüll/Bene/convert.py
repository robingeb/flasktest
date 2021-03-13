import json
AID = "1"
ANU = "2"
timestamp = "3"
ANA = "4"
name = "5"
mängel = "6"
accept = "7"

payload = "{\r\n    \"id\": \""+str(AID)+"\",\r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleAlternativeQuantities\": [],\r\n    \"articleImages\": [],\r\n    \"articleNumber\": \""+str(ANU)+"\",\r\n    \"articlePrices\": [],\r\n    \"articleType\": \"BASIC\",\r\n    \"availableForSalesChannels\": [],\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"createdDate\": 1610284558822,\r\n    \"customAttributes\": [\r\n        {\r\n            \"attributeDefinitionId\": \"3546\",\r\n            \"dateValue\": "+timestamp+"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3590\",\r\n            \"stringValue\": \""+mängel+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3659\",\r\n            \"stringValue\": \""+name+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3671\",\r\n            \"booleanValue\": "+accept+"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3733\",\r\n            \"numberValue\": \"456\"\r\n        }\r\n    ],\r\n    \"defaultWarehouseLevels\": [],\r\n    \"lastModifiedDate\": 1612977937045,\r\n    \"name\": \""+str(ANA)+"\",\r\n    \"productionArticle\": false,\r\n    \"productionBillOfMaterialItems\": [],\r\n    \"salesBillOfMaterialItems\": [],\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"supplySources\": [],\r\n    \"tags\": [],\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useAvailableForSalesChannels\": false,\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}" 
#s = '{"success": "true", "status": 200, "message": "Hello"}'
d = json.loads(payload)
print(d)