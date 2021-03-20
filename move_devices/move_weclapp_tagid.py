import pandas as pd
import numpy as np
import json
from api.weclapp import *

#   Items müssen vor Testem aus Weclapp wieder gelöscht werden, damit der Import funktioniert
def main():

    # information for Request
    url = " https://wwmeqaovgkvqrzk.weclapp.com/webapp/api/v1/article"
    auth = {
        'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43'
    }

    # initialice WeClappAPI und Geräte-Instanzen als Liste ausgeben
    weClappAPI = WeClappAPI(url, auth)
    machine_instances = get_weclapp(weClappAPI)

    # Datenstruktur von TagIdeasy 
    device, inventar = get_tagideasy()

    result = []

    # Geräte zum API Input-Schema von TagIdeasy mappen
    mapped_inventar, mapped_device = map_attributes(device, inventar, machine_instances)

    # Ausgeben der beiden Listen. Kein Upload da TagIdeasy nicht gegeben.
    print(mapped_inventar)
    print(mapped_device)
    return result


def get_tagideasy():
    with open("tagideasy_json/Datenstruktur_Geräte.json") as f:
        inventar = json.loads(f.read())
    with open("tagideasy_json/Datenstruktur_Inventar.json") as f:
        device = json.loads(f.read())
    return inventar, device

def get_weclapp(weClappAPI):
        # Abrufen aller Artikel
        article_all = weClappAPI.get_request()

        # Aussortieren der nicht zu updatenden Artikel
        machine_instances = []
        for instance in article_all["result"]:
            # Suche nur auf Anlagen eingrenzen (hier Beispielhaft: ArtikelNummer >100 für Anlagen)
            if int(instance["articleNumber"]) >= 1000 & int(instance["articleNumber"]) <2000:
                machine_instances.append(instance)
        return  machine_instances


def map_attributes(inventar, device, machine_instances):

    # Erstellen zweier Listen gemäß der Datenstruktur von TagIdeasy
    instances_inventar = []
    instances_device = []

    for x in range(len(machine_instances)):
        print(x)
        inventar_add = inventar
        device_add = device
        inventar_add["core"]["inventory_number"] = machine_instances[x]["articleNumber"]
        device_add["core"]["device_name"] = machine_instances[x]["name"]
        instances_inventar.append(inventar_add)
        instances_device.append(device_add)
    
    return instances_inventar, instances_device



if __name__ == "__main__":
    main()
