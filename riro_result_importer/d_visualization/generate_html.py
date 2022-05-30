import re
import database as database
import html_templates as template
import pandas as pd
from datetime import datetime

tablename = '2022_Flugsaison_Hirschi'
tablename_eingesetzt = '2022_Eingesetzte_Tauben_Hirschi'
outputfilename = '2022.html'
auswertungsdatum = datetime.now()

# Flüge aus Datenbank importieren
fluege = database.get_fluege(tablename)
fluege = fluege.sort_values(by=['flugnummer'])
print(fluege.to_markdown())

# Aggregierte Einzelresultate aus Datenbank importieren
agg_resultate = database.get_agg_resultate(tablename, tablename_eingesetzt)
agg_resultate = agg_resultate.sort_values(by=['aspkt_rv_total'],ascending=False)
print(agg_resultate.to_markdown())

# Einzelresultate aus Datenbank importieren
resultate = database.get_resultate(tablename, tablename_eingesetzt)
print(resultate.to_markdown())

# Anzahl Fluege abfragen
max_flug = database.get_max_flug(tablename_eingesetzt)
print(max_flug.to_markdown())
max_flug_int = max_flug['max_flug'].values[0]

fileout = open("/Users/ph/Projects/riro/riro_brieftauben_statistiken/riro_result_importer/output/"+outputfilename, "w")

table = "<table id=""result_table"" class=""display"">\n"

# Create the table's column headers
table += "  <thead><tr>\n"
table += "  <th>Taube</th>\n"
counter = 0
for index, row in fluege.iterrows():
    table += "    <th>{0}</th>\n".format((row['auflassort']) + "<br>" + row['km'] 
    + "km - " + row['prs'] + "<br>" + str(row['flugdatum']))
    counter = counter + 1
if counter < max_flug_int:
    diff = max_flug_int - counter
    count = 1
    while diff > 0:
        table += "    <th>{0}</th>\n".format("Flug " + str(counter + count))
        diff = diff - 1
        count = count + 1
table += "  <th>Preise<br>RV</th>\n"
table += "  <th>Preise<br>FG</th>\n"
table += "  <th>AsPkt<br>RV</th>\n"
table += "  <th>AsPkt<br>FG</th>\n"
table += "  </tr></thead>\n"

# Create the table's row data
table += "  </tr><tbody>\n"

for index, row in agg_resultate.iterrows():
    table += "  <tr>\n"
    if row['taubennr'] and row['taubennr'] in ('CH-21-4836w','CH-21-4855','CH-21-4844w','CH-21-4826w','CH-21-4817w'):
        table += "    <td style=""color:#00F;"">{0}</td>\n".format(row['taubennr'])
    else:
        table += "    <td>{0}</td>\n".format(row['taubennr'])
    
    for x in range(max_flug_int):
        resultat = resultate.loc[(resultate['taubennr'] == row['taubennr'])&(resultate['flugnummer'] == x+1)]
        if not resultat.empty:
            resultat = resultat.iloc[0]

            if str(resultat['prs_rv']) == "":
                resultat['prs_rv'] = "-"
            if str(resultat['prs_fg']) == "":
                resultat['prs_fg'] = "-"

            if resultat['prs_zt'] or resultat['prs_rv'] or resultat['prs_fg']:
                table += "    <td>{0}</td>\n".format(str(resultat['prs_zt']) + " / " + str(resultat['prs_rv']) 
                + " / " + str(resultat['prs_fg'])+ "<br>" + str(resultat['aspkt_fg']).replace("nan","-") + " / " 
                + str(resultat['aspkt_rv']).replace("nan","-"))
            else:
                table += "    <td>{0}</td>\n".format("O")
        else:
            table += "    <td>-</td>\n"

    table += "    <td>{0}</td>\n".format(row['prs_rv'])
    table += "    <td>{0}</td>\n".format(row['prs_fg'])
    table += "    <td>{0}</td>\n".format(row['aspkt_rv_total'])
    table += "    <td>{0}</td>\n".format(row['aspkt_fg_total'])
    table += "  </tr>\n"

table += "  </tr></tbody>\n"
table += "</table>"

fileout.writelines(template.INTRO + table + template.OUTRO)
fileout.close()