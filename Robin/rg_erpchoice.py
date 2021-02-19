from flask import Flask, render_template, url_for, render_template, request, redirect
from rg_forms import choiceform, erpform
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify

app = Flask(__name__,template_folder = 'templates')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True
urlget = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
#payload="{            \r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleNumber\": \"002\",\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"customAttributes\": [\r\n    {\r\n        \"attributeDefinitionId\": \"3546\",\r\n        \"dateValue\": 1613602800000\r\n    },\r\n    {\r\n        \"attributeDefinitionId\": \"3590\",\r\n        \"stringValue\": \"pizzaa\"\r\n    }\r\n],\r\n    \"name\": \""+ANA+"\",\r\n    \"productionArticle\": false,\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}       "
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'AuthenticationToken': '22cca5be-4270-4f2d-9412-e7b582b4a85d',
  'Cookie': '_sid_=1'
}
@app.route('/')
def home():
    return 'Home'

@app.route('/choice', methods=['GET', 'POST'])
def index():
    name = None
    form = choiceform()
    return render_template('choice.html', form = form, name = name)
    







if __name__ == '__main__':
    app.run(debug=True)



