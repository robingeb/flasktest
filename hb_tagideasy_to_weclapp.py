import pandas as pd
import numpy as np
import json
from hb_weclapp import *

#   Items müssen vor Testem aus Weclapp wieder gelöscht werden, damit der Import funktioniert 

def main():
    

    # information for Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
    'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }
    weclapp_article_attributes =["articleNumber","name","unitId" ]

    result = []
    x,y = get_tagideasy()
    devices_mapped = map_attributes(x,y, weclapp_article_attributes)

    
    # initialice WeClappAPI
    weClappAPI = WeClappAPI(url, auth)

    #TODO: Existiert möglichkeit mehrere Artikel auf einmal zu pushen?
    
    # Iterate throug articles and push them to weclapp
    for index, row in devices_mapped.iterrows():
        df_article = pd.DataFrame([row], columns= weclapp_article_attributes)
        # transform to json
        result_json = df_article.to_json(orient="records")
        parsed = json.loads(result_json) [0]
        final_json = json.dumps(parsed, indent=4)
        print(final_json)
        # push single articles to weclapp
        r = weClappAPI.post_request(final_json)
        result.append(r)
    print(result)

def get_tagideasy():
    with open("1_example_inventar.json") as f:
        inventar = json.loads(f.read()) 
    with open("1_example_geraete.json") as f:
        device = json.loads(f.read())
    return inventar, device
    
def map_attributes(inventar, device, weclapp_article_attributes):    
    

    # get serial number from v1_inventar and match as articel number
    article_number = [inventar["results"][x]["core"]["serial_number"] for x in range(len(inventar["results"]))]
    
    # get article id to identify the device-categorie in geräte_v1
    article_id = [inventar["results"][x]["core"]["articel_id_buyer"] for x in range(len(inventar["results"]))]

    # get device name from geräte_v1 with help of the article id
    device_name =[]
    for x in range(len(inventar["results"])):
        for y in range(len(device["results"])):
            if device["results"][y]["core"]["articel_id_manufacturer"] == article_id[x]:
                device_name.append(device["results"][y]["core"]["device_name"])

    # generate unit_id (2895 for Stk. )
    id = 2895
    unit_id = [id] * len(article_id)

    articles = np.array([article_number, device_name, unit_id])
    articles = articles.transpose()
    df_articles = pd.DataFrame(articles, columns= weclapp_article_attributes)
    #result_json = df_articles.to_json(orient="records")
    return df_articles
      

if __name__ == "__main__":
    main()
