
import requests

url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"

payload="""
{
    "id": "3332",
    "version": "1",
    "active": true,
    "applyCashDiscount": true,
    "articleAlternativeQuantities": [],
    "articleImages": [],
    "articleNumber": "008",
    "articlePrices": [],
    "articleType": "STORABLE",
    "availableForSalesChannels": [],
    "availableInSale": true,
    "availableInShop": false,
    "batchNumberRequired": false,
    "billOfMaterialPartDeliveryPossible": false,
    "createdDate": 1610284455237,
    "customAttributes": [],
    "defaultWarehouseLevels": [],
    "description": "<p>Erstellt zum Testen der eines Api zugriffs</p>",
    "lastModifiedDate": 1610284455276,
    "marginCalculationPriceType": "PURCHASE_PRICE_PRODUCTION_COST",
    "name": "Fahrradsitz",
    "productionArticle": false,
    "productionBillOfMaterialItems": [],
    "salesBillOfMaterialItems": [],
    "serialNumberRequired": false,
    "showOnDeliveryNote": true,
    "supplySources": [],
    "tags": [],
    "taxRateType": "STANDARD",
    "unitId": "2895",
    "unitName": "Stk.",
    "useAvailableForSalesChannels": false,
    "useSalesBillOfMaterialItemPrices": false,
    "useSalesBillOfMaterialItemPricesForPurchase": false
}"""
#payload="{\r\n    \"id\": \"3332\",\r\n    \"version\": \"1\",\r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleAlternativeQuantities\": [],\r\n    \"articleImages\": [],\r\n    \"articleNumber\": \"005\",\r\n    \"articlePrices\": [],\r\n    \"articleType\": \"STORABLE\",\r\n    \"availableForSalesChannels\": [],\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"createdDate\": 1610284455237,\r\n    \"customAttributes\": [],\r\n    \"defaultWarehouseLevels\": [],\r\n    \"description\": \"<p>Erstellt zum Testen der eines Api zugriffs</p>\",\r\n    \"lastModifiedDate\": 1610284455276,\r\n    \"marginCalculationPriceType\": \"PURCHASE_PRICE_PRODUCTION_COST\",\r\n    \"name\": \"Fahrraddynamo2\",\r\n    \"productionArticle\": false,\r\n    \"productionBillOfMaterialItems\": [],\r\n    \"salesBillOfMaterialItems\": [],\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"supplySources\": [],\r\n    \"tags\": [],\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useAvailableForSalesChannels\": false,\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43',
  'Cookie': '_sid_=1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
