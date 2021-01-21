import requests
import xmltodict
from flask import jsonify

url = "https://cloud.myfactory.com/myfactory/odata_lusajejalimimajoyuso52/Artikel"
auth = {
  'username': 'HB',
  "password": "HB"
}

# payload="""{
#         <d:PK_ArtikelID m:type="Edm.Int32">22</d:PK_ArtikelID>
#         <d:Artikelnummer>001</d:Artikelnummer>
#         <d:Kurzbezeichnung>Fahrrad1 „SprintCity“</d:Kurzbezeichnung>
#         <d:KurzbezeichnungZusatz></d:KurzbezeichnungZusatz>
#         <d:Basismenge>Stk</d:Basismenge>
#         <d:FK_ArtikelgruppeKurz>Sonstiges</d:FK_ArtikelgruppeKurz>
#         <d:Hersteller></d:Hersteller>
#         <d:Bezeichnung>E-Scooter „SprintCity“ LB</d:Bezeichnung>
#         <d:BezeichnungZusatz></d:BezeichnungZusatz>
#         <d:Artikeltyp>Stückliste</d:Artikeltyp>
#         <d:FK_HauptlieferantID m:type="Edm.Int32">0</d:FK_HauptlieferantID>
#         <d:Mindestdispositionsmenge m:type="Edm.Double">0</d:Mindestdispositionsmenge>
#         <d:ABC_Klasse>C</d:ABC_Klasse>
#         <d:Inaktiv m:type="Edm.Int32">0</d:Inaktiv>
#         <d:Artikelstatus></d:Artikelstatus>
#         <d:Statustext></d:Statustext>
#         <d:Ursprungsland></d:Ursprungsland>
#         <d:EANNummer></d:EANNummer>
#         <d:Zolltarifnummer></d:Zolltarifnummer>
#         <d:Anlagedatum m:type="Edm.DateTime">2020-05-20T12:45:22.187</d:Anlagedatum>
#         <d:FK_AnlagebenutzerKurz>LB003</d:FK_AnlagebenutzerKurz>
#         <d:Aenderungsdatum m:type="Edm.DateTime">2020-05-20T12:48:43.887</d:Aenderungsdatum>
#         <d:FK_AenderungsbenutzerKurz>LB003</d:FK_AenderungsbenutzerKurz>
#         <d:IstWebshopartikel m:type="Edm.Int32">0</d:IstWebshopartikel>
#         <d:FK_HauptlagerortID m:type="Edm.Int32">0</d:FK_HauptlagerortID>
#         <d:Gewicht m:type="Edm.Double">0</d:Gewicht>
#         <d:Gewichteinheit></d:Gewichteinheit>
#         <d:Meldebestand m:type="Edm.Double">0</d:Meldebestand>
#         <d:VKME></d:VKME>
#         <d:MEfuerPreisangaben></d:MEfuerPreisangaben>
#         <d:Verkaufspreisbasis></d:Verkaufspreisbasis>
#         <d:Gebindemenge m:type="Edm.Double">0</d:Gebindemenge>
#         <d:PAngVMEenthBME m:type="Edm.Double">0</d:PAngVMEenthBME>
#         <d:Gesamtlagerbestand m:null="true" />
#         <d:MittlererEKPreis m:null="true" />
#         <d:LetzterEKPreis m:null="true" />
#         <d:WertDurchscnnittlicherEK m:null="true" />
#         <d:WertDurchschnittlicherBestand m:null="true" />
#         <d:KalkulatorischerEK m:null="true" />
#         <d:KalkulatorischerEK2 m:null="true" />
#         <d:InternerWert m:null="true" />
#         <d:WertDurchschnittlicheProduktion m:null="true" />
#         <d:WertLetzteProduktion m:null="true" />
#         <d:D_Bezeichnung m:null="true" />
#         <d:D_BezeichnungZusatz m:null="true" />
#         <d:D_Langtext m:null="true" />
#         <d:D_Dimensionstext m:null="true" />
#         <d:D_Zusatztext m:null="true" />
#         <d:E_Bezeichnung m:null="true" />
#         <d:E_BezeichnungZusatz m:null="true" />
#         <d:E_Langtext m:null="true" />
#         <d:E_Dimensionstext m:null="true" />
#         <d:E_Zusatztext m:null="true" />
# }"""

def get_request():
    response = requests.request("GET", url, auth=(auth['username'], auth['password']))    
    content_dict = xmltodict.parse(response.text)
    #return jsonify(content_dict)
    print(content_dict)
    
def post_request():
    """Datenimport ist leider nicht möglich. Nur lesender Zugriff über API erlaubt. Alternative: Datenimport von MyFactory. 
    Daten werden von unserem Tool in das benötigten Format transformiert und können dann händisch importiert werden """
    #response = requests.request("POST", url, auth=(auth['username'], auth['password']), data=payload)
    #print(response.text)
    pass
    

def delete_request():
    """Delete-Request ebenfalls nicht möglich"""
    pass


if __name__ == "__main__":
    get_request()