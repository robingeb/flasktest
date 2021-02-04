from flask import Flask, render_template, url_for, render_template, request
from rg_forms import NameForm
import requests
from datetime import datetime, date, timezone

#interner Systemname Test: icnad98qpdoq31

app = Flask(__name__,template_folder = 'templates')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['CSRF_ENABLED'] = True
url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article/id/3340"
Artikelname="Fahrrasdfad"
payload="{            \r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleNumber\": \"002\",\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"customAttributes\": [\r\n    {\r\n        \"attributeDefinitionId\": \"3546\",\r\n        \"dateValue\": 1613602800000\r\n    },\r\n    {\r\n        \"attributeDefinitionId\": \"3590\",\r\n        \"stringValue\": \"pizzaa\"\r\n    }\r\n],\r\n    \"name\": \""+Artikelname+"\",\r\n    \"productionArticle\": false,\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}       "
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
    if form.validate_on_submit():
        #nächstes Prüfdatum übertragen:
        #date2 aus Formular holen: date zu datetime konvertieren -> datetime zu unixtime (float) konvertieren -> float in int konvertieren (um Nachkommastellen zu entfernen) -> int in String konvertireren und 3 nullen dranhängen
            
        date2 = form.date2.data
        dt = datetime.combine(date2, datetime.min.time())
        #Var timestamp wird in payload benutzt
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
        timestamp = int(timestamp)
        timestamp = str(timestamp) + "000"

        name = form.name.data
        print(name)
        print(type(name))
        
        mängel = form.mängel.data

        accept = form.accept.data
        accept = str(accept)
        print(accept)
        

        payload="{            \r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleNumber\": \"002\",\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"customAttributes\": [\r\n    {\r\n    \"attributeDefinitionId\": \"3546\",\r\n        \"dateValue\": "+timestamp+"\r\n    },\r\n    {\r\n        \"attributeDefinitionId\": \"3590\",\r\n        \"stringValue\": \""+name+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3659\",\r\n            \"stringValue\": \""+mängel+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3671\",\r\n            \"booleanValue\": "+accept+"\r\n        }\r\n    ],\r\n     \"name\": \""+Artikelname+"\",\r\n    \"productionArticle\": false,\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n  \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}       "
        
        #print(timestamp)
        print("erfolgreich")
        requests.request("PUT", url, headers=headers, data=payload)
    else: print('false')

    return render_template('signup.html', form=form, name=name)


if __name__ == '__main__':
    app.run(debug=True)






    # API Zusatzfelder
    

# vielen Dank für Ihre Nachricht.

# Die Zusatzfelder befinden Sie im Abschnitt  "customAttributes", bei einer Einfachauswahl sieht das ganze dann beispielhaft so aus: 
#    {
#       "attributeDefinitionId": "152696",
#       "selectedValueId": "152707"
#     }
# Um alle möglichen IDs für die Zusatzfelder zu erhalten kann man einen GET auf /webapp/api/v1/customAttributeDefinition durchführen. Hier erhält man dann die möglichen Werte. 
# Ein Filtern auf einen bestimmten Kunden ist über die ID des Kunden möglich. 

# Freundliche Grüße
# Florian Neuhaus
# Customer Success

# >>> import time
# >>> import datetime
# >>> s = "01/12/2011"
# >>> time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
# 1322697600.0