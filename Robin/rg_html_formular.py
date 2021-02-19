from flask import Flask, render_template, url_for, render_template, request, redirect
from rg_forms import NameForm, articleForm
import requests
from datetime import datetime, date, timezone
import json
from flask import jsonify

#interner Systemname Test: icnad98qpdoq31

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

@app.route('/article', methods=['GET', 'POST'])
def index():
    name = None
    form = articleForm()

    response = requests.request("GET", urlget, headers=headers) #data = payload
    data = json.loads(response.text)
    #Filtert und sortiert Daten
    articleid = [data["result"][x]["id"] for x in range(len(data["result"]))]
    #print(type(articleid))
    articlenumber = [data["result"][x]["articleNumber"] for x in range(len(data["result"]))]
    articlename = [data["result"][x]["name"] for x in range(len(data["result"]))]
    #print(type(articlenumber))
    
    if form.validate_on_submit():
        counter = 0
        Artikelnr = form.Artikelnummer.data
        print(Artikelnr)
        print(type(Artikelnr))
        matchnumber = 0
        for x in articlenumber:
            if x == Artikelnr:
                matchnumber = counter
            counter = counter + 1
        
        AID = articleid[matchnumber]
        ANA = articlename[matchnumber]
        ANU = articlenumber[matchnumber]
        liste = str(AID) + "," + str(ANA) + "," + str(ANU)

        
        return redirect(url_for('signup', liste=liste))
    
    
   
    #return jsonify(data)  
    return render_template('index.html', form=form, name=name)






@app.route('/formular/<string:liste>', methods=['GET', 'POST'])
def signup(liste):
    liste = liste.split(",")
    AID = liste[0]
    ANA = liste[1]
    ANU = liste[2]
    name = None
    form = NameForm()
    url = "https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article/id/"+str(AID)
    print(url)
    if form.validate_on_submit():
        
        #ID des Prüfers (INT)
        #WIRD NOCH NICHT ÜBERTRAGEN
        ID = form.ID.data
        ID = str(ID)
        
        #nächstes Prüfdatum übertragen:
        #date2 aus Formular holen: date zu datetime konvertieren -> datetime zu unixtime (float) konvertieren -> float in int konvertieren (um Nachkommastellen zu entfernen) -> int in String konvertireren und 3 nullen dranhängen    
        date2 = form.date2.data
        dt2 = datetime.combine(date2, datetime.min.time())

        dt = form.date1.data


    
        #Var timestamp wird in payload benutzt
        timestamp = dt2.replace(tzinfo=timezone.utc).timestamp()
        timestamp = int(timestamp)
        timestamp = str(timestamp) + "000"
        
        timestamp2 = dt.replace(tzinfo=timezone.utc).timestamp()
        timestamp2 = int(timestamp2)
        timestamp2 = str(timestamp2) + "000"
        print(timestamp2)

         

        #Name des Prüfers (String)
        name = form.name.data
       
        #Mängel (Textfield)
        mängel = form.mängel.data

        #Gerät bestanden (bool)
        accept = form.accept.data
        accept = str(accept)
        

        print(AID)
        print(ANU)
        print(ANA)
        #payload="{\r\n    \"id\": \"3340\",\r\n    \"version\": \"30\",\r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleAlternativeQuantities\": [],\r\n    \"articleImages\": [],\r\n    \"articleNumber\": \"002\",\r\n    \"articlePrices\": [],\r\n    \"articleType\": \"BASIC\",\r\n    \"availableForSalesChannels\": [],\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"createdDate\": 1610284558822,\r\n    \"customAttributes\": [\r\n        {\r\n            \"attributeDefinitionId\": \"3546\",\r\n            \"dateValue\": 1602280800000\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3590\",\r\n            \"stringValue\": \"test\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3659\",\r\n            \"stringValue\": \"test\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3671\",\r\n            \"booleanValue\": true\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3733\",\r\n            \"numberValue\": \"456\"\r\n        }\r\n    ],\r\n    \"defaultWarehouseLevels\": [],\r\n    \"lastModifiedDate\": 1612977937045,\r\n    \"name\": \"Fahrrasdfad\",\r\n    \"productionArticle\": false,\r\n    \"productionBillOfMaterialItems\": [],\r\n    \"salesBillOfMaterialItems\": [],\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"supplySources\": [],\r\n    \"tags\": [],\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useAvailableForSalesChannels\": false,\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}"
        payload="{\r\n    \"id\": \""+str(AID)+"\",\r\n    \"active\": true,\r\n    \"applyCashDiscount\": true,\r\n    \"articleAlternativeQuantities\": [],\r\n    \"articleImages\": [],\r\n    \"articleNumber\": \""+str(ANU)+"\",\r\n    \"articlePrices\": [],\r\n    \"articleType\": \"BASIC\",\r\n    \"availableForSalesChannels\": [],\r\n    \"availableInSale\": true,\r\n    \"availableInShop\": false,\r\n    \"batchNumberRequired\": false,\r\n    \"billOfMaterialPartDeliveryPossible\": false,\r\n    \"createdDate\": 1610284558822,\r\n    \"customAttributes\": [\r\n        {\r\n            \"attributeDefinitionId\": \"3546\",\r\n            \"dateValue\": "+timestamp+"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3590\",\r\n            \"stringValue\": \""+mängel+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3659\",\r\n            \"stringValue\": \""+name+"\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3671\",\r\n            \"booleanValue\": "+accept+"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"3733\",\r\n            \"numberValue\": \"456\"\r\n        },\r\n        {\r\n            \"attributeDefinitionId\": \"4188\",\r\n            \"dateValue\": "+timestamp2+"\r\n        }\r\n    ],\r\n    \"defaultWarehouseLevels\": [],\r\n    \"lastModifiedDate\": 1612977937045,\r\n    \"name\": \""+str(ANA)+"\",\r\n    \"productionArticle\": false,\r\n    \"productionBillOfMaterialItems\": [],\r\n    \"salesBillOfMaterialItems\": [],\r\n    \"serialNumberRequired\": false,\r\n    \"showOnDeliveryNote\": true,\r\n    \"supplySources\": [],\r\n    \"tags\": [],\r\n    \"taxRateType\": \"STANDARD\",\r\n    \"unitId\": \"2895\",\r\n    \"unitName\": \"Stk.\",\r\n    \"useAvailableForSalesChannels\": false,\r\n    \"useSalesBillOfMaterialItemPrices\": false,\r\n    \"useSalesBillOfMaterialItemPricesForPurchase\": false\r\n}"        
        print("erfolgreich")
        print(requests.request("PUT", url, headers=headers, data=payload))
        
    else: print('nicht erfolgreich')

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