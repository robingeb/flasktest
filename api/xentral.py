import xmltodict
#from flask import jsonify
import requests
import json
from requests.auth import HTTPDigestAuth

def test(payload = None):
    url = " http://132.187.226.135/www/api//index.php/v1/artikel"
    auth = {
    'username': 'HB',
    "password": "HB"
    }
    xentralApi = XentralAPI(url, auth)
    xentralApi.get_request()

class XentralAPI():
    """
    Zugriff auf die Api von Xentral. 

    :param str url: gültige Zugangsurl zu Dynamics
    :param dict auth: Authentifizierungsdaten Form: {"username": string, "password": string } 
    """
    def __init__(self, url, auth):        
        self.url = url
        self.auth = auth

   
    def get_request(self):
        """
        Führt einen GET-Request durch.

        :return: ein Dictionary mit Ergebniss des Requests.
        """  
        response = requests.request("GET", self.url, auth=HTTPDigestAuth(self.auth['username'], self.auth['password']))
        data = json.loads(response.text)
        return data 
        
    def post_request(self):
         """
        -------------POST-Request funktioniert nicht---------------------
        Führt einen POST-Request durch.

        :param json payload:  als json formatierter string mit zur hinzufügenden Instanz.
        :return: ein Dictionary mit Instanz, welche nach Dynamics geladen wurde.
        """  
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
             #'AuthenticationToken': '837196b1-b252-4bc2-98e4-d7a4f9250a43',
            'Cookie': '_sid_=1'
            }
        response = requests.request("POST", self.url, headers = headers, auth=HTTPDigestAuth(self.auth['username'], self.auth['password']), data=self.payload)
        return response.text

    def put_request(self):
        pass
        # TODO: Put Request testen

payload = """
{        
            "id": "",
            "typ": "",
            "marketingsperre": "",
            "trackingsperre": "0",
            "rechnungsadresse": "0",
            "sprache": "",
            "name": "",
            "abteilung": "",
            "unterabteilung": "",
            "ansprechpartner": "",
            "land": "",
            "strasse": "",
            "ort": "",
            "plz": "",
            "telefon": "",
            "telefax": "",
            "mobil": "",
            "email": "",
            "ustid": "",
            "ust_befreit": "0",
            "passwort_gesendet": "0",
            "sonstiges": "",
            "adresszusatz": "",
            "kundenfreigabe": "0",
            "steuer": "",
            "logdatei": "2021-01-28 17:45:16",
            "kundennummer": "",
            "lieferantennummer": "",
            "mitarbeiternummer": "",
            "konto": "",
            "blz": "",
            "bank": "",
            "inhaber": "",
            "swift": "",
            "iban": "",
            "waehrung": "",
            "paypal": "",
            "paypalinhaber": "",
            "paypalwaehrung": "",
            "projekt": "1",
            "partner": "0",
            "zahlungsweise": "rechnung",
            "zahlungszieltage": "",
            "zahlungszieltageskonto": "",
            "zahlungszielskonto": "",
            "versandart": "versandunternehmen",
            "kundennummerlieferant": "",
            "zahlungsweiselieferant": "rechnung",
            "zahlungszieltagelieferant": "",
            "zahlungszieltageskontolieferant": "",
            "zahlungszielskontolieferant": "",
            "versandartlieferant": "",
            "geloescht": "0",
            "firma": "1",
            "webid": "",
            "vorname": "",
            "kennung": "",
            "sachkonto": "",
            "freifeld1": "",
            "freifeld2": "",
            "freifeld3": "",
            "filiale": "",
            "vertrieb": "",
            "innendienst": "",
            "verbandsnummer": "",
            "abweichendeemailab": "",
            "portofrei_aktiv": "",
            "portofreiab": "0.00",
            "infoauftragserfassung": "",
            "mandatsreferenz": "",
            "mandatsreferenzdatum": "",
            "mandatsreferenzaenderung": "0",
            "glaeubigeridentnr": "",
            "kreditlimit": "0.00",
            "tour": "0",
            "zahlungskonditionen_festschreiben": "",
            "rabatte_festschreiben": "",
            "mlmaktiv": "",
            "mlmvertragsbeginn": "",
            "mlmlizenzgebuehrbis": "",
            "mlmfestsetzenbis": "",
            "mlmfestsetzen": "0",
            "mlmmindestpunkte": "0",
            "mlmwartekonto": "0.00",
            "abweichende_rechnungsadresse": "0",
            "rechnung_vorname": "",
            "rechnung_name": "",
            "rechnung_titel": "",
            "rechnung_typ": "",
            "rechnung_strasse": "",
            "rechnung_ort": "",
            "rechnung_plz": "",
            "rechnung_ansprechpartner": "",
            "rechnung_land": "",
            "rechnung_abteilung": "",
            "rechnung_unterabteilung": "",
            "rechnung_adresszusatz": "",
            "rechnung_telefon": "",
            "rechnung_telefax": "",
            "rechnung_anschreiben": "",
            "rechnung_email": "",
            "geburtstag": "",
            "rolledatum": "",
            "liefersperre": "",
            "liefersperregrund": "",
            "mlmpositionierung": "",
            "steuernummer": "",
            "steuerbefreit": "",
            "mlmmitmwst": "",
            "mlmabrechnung": "",
            "mlmwaehrungauszahlung": "",
            "mlmauszahlungprojekt": "0",
            "sponsor": "",
            "geworbenvon": "",
            "logfile": "",
            "kalender_aufgaben": "",
            "verrechnungskontoreisekosten": "0",
            "usereditid": "",
            "useredittimestamp": "0000-00-00 00:00:00",
            "rabatt": "",
            "provision": "",
            "rabattinformation": "",
            "rabatt1": "",
            "rabatt2": "",
            "rabatt3": "",
            "rabatt4": "",
            "rabatt5": "",
            "internetseite": "",
            "bonus1": "",
            "bonus1_ab": "",
            "bonus2": "",
            "bonus2_ab": "",
            "bonus3": "",
            "bonus3_ab": "",
            "bonus4": "",
            "bonus4_ab": "",
            "bonus5": "",
            "bonus5_ab": "",
            "bonus6": "",
            "bonus6_ab": "",
            "bonus7": "",
            "bonus7_ab": "",
            "bonus8": "",
            "bonus8_ab": "",
            "bonus9": "",
            "bonus9_ab": "",
            "bonus10": "",
            "bonus10_ab": "",
            "rechnung_periode": "",
            "rechnung_anzahlpapier": "",
            "rechnung_permail": "",
            "titel": "",
            "anschreiben": "",
            "nachname": "",
            "arbeitszeitprowoche": "0.00",
            "folgebestaetigungsperre": "0",
            "lieferantennummerbeikunde": "",
            "verein_mitglied_seit": "",
            "verein_mitglied_bis": "",
            "verein_mitglied_aktiv": "",
            "verein_spendenbescheinigung": "0",
            "freifeld4": "",
            "freifeld5": "",
            "freifeld6": "",
            "freifeld7": "",
            "freifeld8": "",
            "freifeld9": "",
            "freifeld10": "",
            "rechnung_papier": "0",
            "angebot_cc": "",
            "auftrag_cc": "",
            "rechnung_cc": "",
            "gutschrift_cc": "",
            "lieferschein_cc": "",
            "bestellung_cc": "",
            "angebot_fax_cc": "",
            "auftrag_fax_cc": "",
            "rechnung_fax_cc": "",
            "gutschrift_fax_cc": "",
            "lieferschein_fax_cc": "",
            "bestellung_fax_cc": "",
            "abperfax": "0",
            "abpermail": "",
            "kassiereraktiv": "0",
            "kassierernummer": "",
            "kassiererprojekt": "0",
            "portofreilieferant_aktiv": "0",
            "portofreiablieferant": "0.00",
            "mandatsreferenzart": "",
            "mandatsreferenzwdhart": "",
            "serienbrief": "0",
            "kundennummer_buchhaltung": "",
            "lieferantennummer_buchhaltung": "",
            "lead": "0",
            "zahlungsweiseabo": "",
            "bundesland": "",
            "mandatsreferenzhinweis": "",
            "geburtstagkalender": "0",
            "geburtstagskarte": "0",
            "liefersperredatum": "",
            "umsatzsteuer_lieferant": "",
            "lat": "",
            "lng": "",
            "art": "",
            "fromshop": "0",
            "freifeld11": "",
            "freifeld12": "",
            "freifeld13": "",
            "freifeld14": "",
            "freifeld15": "",
            "freifeld16": "",
            "freifeld17": "",
            "freifeld18": "",
            "freifeld19": "",
            "freifeld20": "",
            "angebot_email": "",
            "auftrag_email": "",
            "rechnungs_email": "",
            "gutschrift_email": "",
            "lieferschein_email": "",
            "bestellung_email": "",
            "lieferschwellenichtanwenden": "0",
            "hinweistextlieferant": "",
            "firmensepa": "0",
            "hinweis_einfuegen": "",
            "anzeigesteuerbelege": "0",
            "gln": "",
            "rechnung_gln": "",
            "keinealtersabfrage": "0",
            "lieferbedingung": "",
            "mlmintranetgesamtestruktur": "0",
            "kommissionskonsignationslager": "0",
            "zollinformationen": "",
            "bundesstaat": "",
            "rechnung_bundesstaat": ""
}"""


if __name__ == "__main__":
    start()

    