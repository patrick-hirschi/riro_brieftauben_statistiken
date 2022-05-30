from bs4 import BeautifulSoup
from asyncio import sleep
import requests
import random
import time
import pywhatkit
from datetime import datetime

# PRODUCTION - PRoductive WhatsApp Group with all Recipients
Gruppenname_Whatsapp = "JIWh8yPyJhTpAkib"

# TESTING - WhatsApp Group with only Developers Account in it
# Uncomment for Testing and Debugging
# Gruppenname_Whatsapp = "IqInOYWK3VjV6J"

# Configuration Values - for Swiss Races only the calendar week and the year have to be adjusted accordingly
regv = "001Schweizer Verband"
filter = "alle"
kw = "21"
year = "2022"
action = "showRaceResults"
alert_state_at_script_start = False

# Build URL
url = f"http://www.bas-riro.de/Preislisten/index.php?regv={regv}&filter={filter}&kw={kw}&year={year}&action={action}"

# Set a Request Header's User Agent
payload = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# List of all RegV's that need to be tracked
regvnames_all = ["RegV 02 (Kr.02) -CH-", "RegV 02 (Kr.03) -CH-", "RegV 04 (Kr.01) -CH-", 
            "RegV 04 (Kr.02) -CH-", "RegV Mitte (K1) -CH-", "RegV Mitte (K3) -CH-",
            "RegV 01 (Ost-K1)-CH-", "RegV 01 (Ost-K3)-CH-", "RegV 01 (Kr.01) -CH-",
            "RegV 01 (Kr.02) -CH-", "RegV 04 (Kr.03) -CH-", "Fribourg Süd CH",
            "Fribourg Mitte CH", "Lausanne", "Geneve", "Fribourg Nord -CH-"]

# Copy the list once because we want to conditionally modify one of the lists during the loop
regvnames = regvnames_all.copy()

# Translate the regvnames to prevent any special characters like e.g. -().
regvnames_translations = {
  "RegV 02 (Kr.02) -CH-":"RegV 02 Kr 02",
  "RegV 02 (Kr.03) -CH-":"RegV 02 Kr 03",
  "RegV 04 (Kr.01) -CH-":"RegV 04 Kr 01",
  "RegV 04 (Kr.02) -CH-":"RegV 04 Kr 02",
  "RegV Mitte (K1) -CH-":"RegV Mitte K1", 
  "RegV Mitte (K3) -CH-":"RegV Mitte K3", 
  "RegV 01 (Ost-K1)-CH-":"RegV 01 Ost K1", 
  "RegV 01 (Ost-K3)-CH-":"RegV 01 Ost K3",
  "RegV 01 (Kr.01) -CH-":"RegV 01 Kr 01", 
  "RegV 01 (Kr.02) -CH-":"RegV 01 Kr 02", 
  "RegV 04 (Kr.03) -CH-":"RegV 04 Kr 03",
  "Fribourg Süd CH":"Fribourg Sued", 
  "Fribourg Mitte CH":"Fribourg Mitte", 
  "Lausanne":"Lausanne", 
  "Geneve":"Geneve",  
  "Fribourg Nord -CH-":"Fribourg Nord"
}

# Instantiate empty lists
vorab_rankings = []
vorab_rankings_delivered = []
final_rankings = []
final_rankings_delivered = []

# Search for "Vorab Rankings" in a BeautifulSoup HTML document
# Return True if available, false if not
def find_vorab_ranking(html_doc, regvname):
    if html_doc.find("td", text=regvname):
        return True
    else:
        return False

# Search for "Final Rankings" in a BeautifulSoup HTML document
# Return True if available, false if not
def find_final_ranking(html_doc, regvname):
    if html_doc.find("a", text=regvname):
        return True
    else:
        return False

count = 0

# Loop as long as not all regvnames were detected with a final ranking
while len(regvnames) > 0:

    # Query the riro URL to check for new rankings later
    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Boolean indicating if a new object was found for a regvname
    change_detected = False

    # Loop through all regvnames
    for regvname in regvnames_all:

        # Check if for a specific regvname a Vorab Ranking is available, if yes, add it to a 
        # new list (avoid delivering alerts multiple times) and set change_detected True.
        if find_vorab_ranking(soup,regvname) and regvname not in vorab_rankings_delivered:
            vorab_rankings.append(regvnames_translations.get(regvname))
            vorab_rankings_delivered.append(regvname)
            change_detected = True

        # Check if for a specific regvname a Final Ranking is available, if yes, add it to a 
        # new list (avoid delivering alerts multiple times) and set change_detected True.
        if find_final_ranking(soup,regvname) and regvname not in final_rankings_delivered:
            final_rankings.append(regvnames_translations.get(regvname))
            final_rankings_delivered.append(regvname)
            change_detected = True
            regvnames.remove(regvname)

    # If any new object was detected in the loop above we need to alert it to the configured recipient
    if change_detected:
        now = datetime.now()
        output = ""
        # Build output text for detected Vorab Rankings
        if len(vorab_rankings) > 0:
            output += "Neuer Ywischenstand vorhanden"
            output += " \n"
            output += "Vorab Rangliste neu vorhanden bei "
            output += ', '.join(vorab_rankings)
        # Build output text for detected Final Rankings
        if len(final_rankings) > 0:
            output += ". \n"
            output += "Finale Rangliste neu vorhanden bei "
            output += " \n"
            output += ', '.join(final_rankings)
        
        # Only alert the state at script start, if it is configured to True
        if count != 0 or alert_state_at_script_start:
            # Send the output text to the recipient via WhatsApp
            pywhatkit.sendwhatmsg_to_group(Gruppenname_Whatsapp, output, now.hour, now.minute + 1, 10, 5)
        
        # Also print it to console
        print(output)

        # Reset the lists holding the findings that now were reported.
        vorab_rankings = []
        final_rankings = []

    # Increase loop counter
    count += 1
       
    # Implement a random delay of 40 to 160 seconds
    sekunden = random.randint(2,4)*random.randint(20,40)
    print(f"Ausführung beendet. --- Schlafe für {sekunden} Sekunden.")
    time.sleep(sekunden)



