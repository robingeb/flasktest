# Es konnte keine Api für den Import von MaschinenDaten gefunden werden. Es existiert ausschließlich eine API für den E-Commerce (Kundenshops, Lieferanten)
# siehe: https://openz.de/handbuch/open-source-erp-einstellungen/konfiguration-reportvorlagen/
# Es existiert in OpenZ eine eigene Anlagenverwaltung, für die aber kein API Zugriff existiert.
#   Daten können über einen Excel Export von OpenZ ausgelesen werden und dann weiterverarbeitet werden
#   Es existiert keine möglichkeit Anlagendaten manuell zu importieren
# Lösungsansatz: Durch Datenexport von OpenZ, Anpassen der Datenstruktur in unserer Middleware und import in TagIDeasy können die Stammdaten dort aktuell gehalten werden. 
# Keine Möglichkeit gefunden Daten von TagIDeasy OpenZ zur Verfügung zu stellen 