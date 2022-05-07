# RIRO Brieftauben Statistiken
Dieses Repository zeigt auf, wie Resultate von Brieftauben-Wettflügen (www.riro.de) in eine Datenbank strukturiert eingelesen und in der Folge analysiert werden können. Der Output ist eine HTML Seite mit einer übersicht über die Leistungen der einzelnen Tauben im jeweiligen Reisejahr.

Ablauf:
1. Kopieren der Preisliste in den Ordner "results"
2. Anpassung der Grundkonfiguration in riro_processor.py
    - zuechter (Züchtername von RIRO)
    - km (Kilometer vom Heimatschlag zum Auflassort)
    - auflassort (Auflassort)
    - flugnr (Wettflugnummer, Bsp. "1" für den ersten des Jahres)
    - flugdatum (Datum des Auflasses)
4. Ausführen des Python Skriptes riro_processor.py
5. Ausführen des Python Skriptes generate_html.py
6. Output html entweder lokal im Browser anschauen oder über einen Webserver hochladen/verfügbar machen
