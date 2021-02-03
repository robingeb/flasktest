from flask import Flask, render_template, url_for, render_template, request
from rg_forms import NameForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article/id/3340"
xy = "5"
payload=" {\r\n            \r\n            \"active\": true,\r\n            \"applyCashDiscount\": true,\r\n            \"articleNumber\": \"002\",\r\n            \"availableInSale\": true,\r\n            \"availableInShop\": false,\r\n            \"batchNumberRequired\": false,\r\n            \"billOfMaterialPartDeliveryPossible\": false,\r\n            \"name\": \"Fahrradreifen"+xy+"\",\r\n            \"productionArticle\": false,\r\n            \"serialNumberRequired\": false,\r\n            \"showOnDeliveryNote\": true,\r\n            \"taxRateType\": \"STANDARD\",\r\n            \"unitId\": \"2895\",\r\n            \"unitName\": \"Stk.\",\r\n            \"useSalesBillOfMaterialItemPrices\": false,\r\n            \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n        }"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'AuthenticationToken': '22cca5be-4270-4f2d-9412-e7b582b4a85d',
  'Cookie': '_sid_=1'
}
@app.route('/')
def home():
    return 'Home'

@app.route('/formular')
def index():
    return render_template('index.html')



@app.route('/eintragen', methods=['GET', 'POST'])
def signup():
    name = None
    form = NameForm()
    if form.validate():
        # name = form.name.data
        # form.name.data = ''
        print("Hello World")
        requests.request("PUT", url, headers=headers, data=payload)
    return render_template('signup.html', form=form, name=name)

if __name__ == '__main__':
    app.run(debug=True)