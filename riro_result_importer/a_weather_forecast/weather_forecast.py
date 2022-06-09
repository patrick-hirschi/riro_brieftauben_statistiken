import csv
import json
import os
from pickletools import pyset
import time
import re
import io
from asyncio import sleep
from contextlib import closing
from datetime import datetime, timedelta
from datetime import timezone
from dateutil import tz
from xmlrpc.server import SimpleXMLRPCRequestHandler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from pandas import DataFrame, json_normalize
from tabulate import tabulate
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfMerger, PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import paramiko
from PIL import Image, ImageDraw, ImageFont

# Configuration Values
api_username = "privat_hirschi"
api_password = "2342334"
ssh_key_password = "3242342354"
start_hour = "07"
hours = 36
resolution_hours = 1
output = "json"
local_basepath = '/Users/ph/Projects/riro/riro_brieftauben_statistiken/riro_result_importer/output/'
remote_basepath = '/home/medizin4/www/patrick-hirschi.ch/wp-content/wetter/'

parameters = {
  "wind_speed":"wind_speed_10m:ms", 
  "wind_direction":"wind_dir_10m:d", 
  "temperature":"t_2m:C", 
  "pressure":"msl_pressure:hPa", 
  "rain":"precip_1h:mm",
  "weather_symbol":"weather_symbol_1h:idx", 
  "uv_index":"uv:idx"
}
locations = {
  "Deggendorf":"48.83250000,13.01341667", 
  "Landau":"48.6828485,12.6920579", 
  "Neufahrn":"48.7333333,12.1833333", 
  "Dachau":"48.31075000,11.56663889", 
  "Dasing":"48.39444444,11.07583333", 
  "Burgau":"48.42908333,10.46283333", 
  "Ulm":"48.47275000,10.05450000",
  "Ehingen":"48.27952778,9.73455556", 
  "Messkirch":"47.99075000,9.03669444", 
  "Konstanz":"47.6779496,9.1732384", 
  "Dielsdorf":"47.48661111,8.45863889", 
  "Luzern":"47.0501682,8.3093072", 
  "Niederbipp":"47.26825000,7.70552778", 
  "Bern":"46.947922,7.444608"
}

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

start_date = next_weekday(datetime.today(), 5)
# Build URL
url = f"https://api.meteomatics.com/{start_date.strftime('%Y-%m-%d')}T{start_hour}ZPT{hours}H:PT{resolution_hours}H/{','.join(parameters.values())}/<<LOCATION>>/{output}"

# session = requests.Session()
# session.auth = (api_username, api_password)

# df_final = pd.DataFrame(columns=['date', 'value', 'data.coordinates.lat', 
#                         'data.coordinates.lon', 'data.parameter', 'city'])

# for key, value in locations.items():
#     location_url = url.replace("<<LOCATION>>",value)

#     # Query the meteomatics webservice URL
#     with session.get(location_url, stream=True) as response:
#         # Use json_normalize() to convert JSON to DataFrame
#         dict = json.loads(response.content)
#         df = json_normalize(dict,
#                                 record_path=['data','coordinates','dates'], 
#                                 meta=[
#                                     ['data','coordinates','lat'], 
#                                     ['data','coordinates','lon'],
#                                     ['data','parameter'],
#                                     ['city']
#                                 ],
#                                 errors='ignore') 
#         df.city = df.city.fillna(key)
#         df_final = pd.concat([df_final, df],ignore_index=True)     

# df_final.to_csv(f"{local_basepath}weather.csv")  

#####
###         READ AND CLEANSE CSV FILE
#####

# read the previously created csv file
weather_data_all_source = pd.read_csv(f"{local_basepath}weather.csv")
# remove special characters from column names
weather_data_all_source.columns = weather_data_all_source.columns.str.replace('[#,@,&,.,_,:]', '', regex=True)
# remove special characters from values in column "dataparameter"
weather_data_all_source["dataparameter"] = weather_data_all_source["dataparameter"].str.replace('[:,_]','',regex=True)

#####
###         CREATE WIND TABLE
#####

# only keep the wind parameters (speed and direction)
weather_data_wind = weather_data_all_source.query("dataparameter=='windspeed10mms' or dataparameter=='winddir10md'").pivot_table(values = 'value', index=['date','city'], columns = 'dataparameter').reset_index()

# add a new column for the textual representation of the wind degrees
weather_data_wind["winddirection"] = " "

# iterate through the dataset, transform the date to local time and calculate the wind direction
for index, row in weather_data_wind.iterrows():
    weather_data_wind.loc[index,'winddirection'] = ["N","NNO","NO","ONO","O","OSO","SO","SSO","S","SSW","SW","WSW","W","WNW","NW","NNW"][round(float(row["winddir10md"])/22.5)%16]
    weather_data_wind.loc[index,'date'] = datetime.fromisoformat(str(row["date"])[:-1]).astimezone(timezone.utc).astimezone(tz.tzlocal()).strftime('%a %d.%m. %H:%M')   

# concatenate speed (transformed from m/s to km/h) and direction into new column "wind"
weather_data_wind["wind"] = round((weather_data_wind["windspeed10mms"]*3.6),1).astype(str) + 'km/h ' + weather_data_wind["winddirection"].astype(str)
weather_data_wind = weather_data_wind.pivot_table(values = 'wind', index='date', columns = 'city',aggfunc=lambda x: ' '.join(x)).reset_index()
# column reordering
weather_data_wind = weather_data_wind[['date', 'Deggendorf', 'Landau', 'Neufahrn', 'Dachau', 'Dasing', 'Burgau', 'Ulm', 'Ehingen', 'Messkirch', 'Konstanz', 'Dielsdorf', 'Luzern', 'Niederbipp', 'Bern']]

#####
###         MATPLOTLIB PLOT WIND TABLE
#####
# https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
fig, ax =plt.subplots(figsize=(12,4))
ax.axis('tight')
ax.axis('off')
colors = []
# Regular expression to extract wind speed and wind direction per cell in the table
pattern  = '^([0-9]*.?[0-9]*)(km\/h)(\s*)([NSWO]*)'
# Color scheme for implementing something like a wind-heatmap
green_color_scheme = ["#C3D986","#9CCC60","#6F9144","#3D650F"]
red_color_scheme = ["#FFC6C6","#FFA0A1","#FF7A7B","#FF5456"]
neutral_color_scheme = ["#E6E6E6","#BFBFBF","#808080","#8C8C8C"]
color_scheme = []

# Loop through the cells to apply a conditional formatting (red scheme for west wind, green scheme 
# for east wind, neutral scheme for everything else and additionally darker colors for higher wind speeds)
for j in range(weather_data_wind.shape[0]): #iterate over row
    colors_in_column = ["w"] * (len(locations) + 1)
    for i in range(weather_data_wind.shape[1]): #iterate over columns
         value = weather_data_wind.iloc[j, i] #get cell value
         match = re.search(pattern, value)
         if match and match.group(2).strip() == 'km/h':
             # Conditional formatting for wind direction (set color scheme)
             if "O" in match.group(4).strip():
                color_scheme = green_color_scheme
             elif "W" in match.group(4).strip():
                color_scheme = red_color_scheme
             else:
                color_scheme = neutral_color_scheme
             wind_speed = float(match.group(1).strip())
             # Conditional Formatting for wind speed (set darkness)
             if wind_speed <= 2.5:
                colors_in_column[i] = color_scheme[0]
             if wind_speed > 2.5 and wind_speed <= 5:
                colors_in_column[i] = color_scheme[1]
             if wind_speed > 5 and wind_speed <= 10:
                colors_in_column[i] = color_scheme[2]
             if wind_speed > 10:
                colors_in_column[i] = color_scheme[3]
    colors.append(colors_in_column)

# prepare the output table
the_table = ax.table(cellText=weather_data_wind.values,colLabels=weather_data_wind.columns,loc='center', cellColours=colors)

#https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
pp = PdfPages("/Users/ph/Projects/riro/riro_brieftauben_statistiken/riro_result_importer/output/Wetterdaten.pdf")
pp.savefig(fig, bbox_inches='tight',
            orientation='landscape',
            papertype='a4')

#####
###         MATPLOTLIB SECTION FOR VISUAL REPRESENTATION
#####

# pivot by data parameters
weather_data_all = weather_data_all_source.pivot_table(values = 'value', index=['date','city'], columns = 'dataparameter').reset_index()

# iterate through the dataset, transform the date to local time
for index, row in weather_data_all.iterrows():
    weather_data_all.loc[index,'date'] = datetime.fromisoformat(str(row["date"])[:-1]).astimezone(timezone.utc).astimezone(tz.tzlocal()).strftime('%a %d.%m. %H:%M')   

#define colors to use
col1 = '#7E8C69'
col2 = '#BD2A2E'
col3 = '#2975D9'
col4 = '#D99B66'


for x in range(1,(len(locations)//5) + 2):
    if x == ((len(locations)//5) + 1):
        #define subplots
        fig,axs = plt.subplots(len(locations)%5,figsize=(50,80),constrained_layout=True)
    else:
        #define subplots
        fig,axs = plt.subplots(5,figsize=(50,80),constrained_layout=True)
    # implement a counter
    count = 1
    # loop through cities and axes
    for city, ax in zip(list(locations.keys())[(x-1)*5:x*5], axs.ravel()):
        if count > 5:
            continue
        # filter df for city
        weather_data = weather_data_all[weather_data_all['city'] == city]

        # chart formatting
        ax.set_title(city.upper(), fontsize=36, fontweight='bold', color='#4E8DA6')
        
        # set grid
        ax.grid(axis="x")
        
        #add first line to plot
        ax.plot(weather_data['date'], round((weather_data["windspeed10mms"]*3.6),1), color=col1, marker=',', linewidth=3)

        #add x-axis label
        ax.set_xticks(ax.get_xticks()) 
        ax.set_xticklabels(weather_data['date'], rotation=90, fontsize=18)

        #add y-axis label
        ax.set_ylim(0,50)
        ax.set_ylabel('Windgeschwindigkeit (km/h)', color=col1, fontsize=18)

        # draw lightgrey boxes for daylights
        day_1 = start_date.strftime('%a %d.%m.')
        day_2 = (start_date + timedelta(days=1)).strftime('%a %d.%m.')
        ax.axvspan(day_1+ " 07:00", day_1 + " 19:00", alpha=1, color='whitesmoke')
        ax.axvspan(day_2+ " 07:00", day_2 + " 19:00", alpha=1, color='whitesmoke')

        #define y-axis that shares x-axis with current plot
        ax2 = ax.twinx()
        ax2.spines["right"].set_position(("axes", 1.03))
        ax2.spines["right"].set_visible(True)

        #add line to plot
        ax2.plot(weather_data['date'], weather_data['t2mC'], color=col2, marker=',', linewidth=2)

        #add y-axis label and lim
        ax2.set_ylim(10,35)
        ax2.set_ylabel('Temperatur (C)', color=col2, fontsize=18)

        #define y-axis that shares x-axis with current plot
        ax3 = ax.twinx()
        ax3.spines["right"].set_position(("axes", 1.06))
        ax3.spines["right"].set_visible(True)

        #add line to plot
        ax3.plot(weather_data['date'], weather_data['precip1hmm'], color=col3, marker=',', linewidth=2)

        #add y-axis label and lim
        ax3.set_ylim(0,15)
        ax3.set_ylabel('Regen (mm)', color=col3, fontsize=18)

        #define y-axis that shares x-axis with current plot
        ax4 = ax.twinx()

        #add line to plot
        ax4.plot(weather_data['date'], weather_data['mslpressurehPa'], color=col4, marker=',', linewidth=2)
        #add y-axis label and lim
        ax4.set_ylim(950,1050)
        ax4.set_ylabel('Luftdruck (hPa)', color=col4, fontsize=18)

        # zip joins x and y coordinates in pairs
        for x,y in zip(weather_data['date'], round((weather_data["windspeed10mms"]*3.6),1)):

            # transform the wind direction from degree to textual representation
            deg = float(weather_data.query("date==@x")['winddir10md'])
            label=str(y)+"\n"+["N","NNO","NO","ONO","O","OSO","SO","SSO","S","SSW","SW","WSW","W","WNW","NW","NNW"][round(deg/22.5)%16]

            ax.annotate(label, # this is the text
                        (x,y), # these are the coordinates to position the label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        fontsize=24, # font-size
                        ha='center') # horizontal alignment can be left, right or center  
        count += 1
    # savefig
    # fig.set_size_inches(8.27,11.69)
    pp.savefig(fig, bbox_inches='tight', pad_inches=1.5)
   

# We can also set the file's metadata via the PdfPages object:
d = pp.infodict()
d['Title'] = 'Brieftauben Wetterdaten'
d['Author'] = 'Patrick Hirschi'
d['CreationDate'] = datetime.now()
d['ModDate'] = datetime.now()

# close pdf stream
pp.close()

#####
###         SET LAST UPDATE TIME IN DOCUMENT PDF
#####
update_date_time = datetime.now()
# Set message to print and the filename
message = f"Zuletzt aktualisiert am {update_date_time.strftime('%d.%m.%Y')} um {update_date_time.strftime('%H:%M:%S')}."

packet = io.BytesIO()

# do whatever writing you want to do
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor("red")
can.setLineWidth(5)
can.drawString(170, 780, message)
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(f"{local_basepath}Wetterreport_Dokumentation.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)

# finally, write "output" to a real file
outputStream = open(f"{local_basepath}Wetterreport_Dokumentation_LASTMOD.pdf", "wb")
output.write(outputStream)
outputStream.close()

#####
###         MERGE PDFs (Documentation & Weather Data)
#####

# Set PDF paths to be combined
pdfs = [f"{local_basepath}Wetterreport_Dokumentation_LASTMOD.pdf", f"{local_basepath}Wetterdaten.pdf"]

# Merge all pages of the configured PDFs
merger = PdfMerger()
for pdf in pdfs:
    merger.append(pdf)
# Write the merged PDF to disk
merger.write(f"{local_basepath}Brieftauben_Wetterreport.pdf")
# Close the PdfMerger
merger.close()

#####
###         CREATE LAST UPDATE DATE TIME IMAGE
#####

filename = f"{local_basepath}last_update_date_time.jpg"

# Draw the text on a JPG image
img = Image.new('RGB', (400, 30), color = "#FFFFFF") 
fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
d = ImageDraw.Draw(img)
d.text((10,10), message, font=fnt, fill="#4575B6")
 
# Save image to disk
img.save(filename)

#####
###         SSH CONNECTION TO HOSTPOINT FOR FILE UPLOAD
#####

# Create SSH client with paramiko
ssh = paramiko.SSHClient()
# Load and decrypt RSA private key for connection
key = paramiko.RSAKey.from_private_key_file('/Users/ph/.ssh/hostpoint_id_rsa', password=ssh_key_password)
# Load the system's known_hosts from /Users/ph/.ssh
ssh.load_system_host_keys()
# Connect to hostpoint webserver
ssh.connect("sl1093.web.hostpoint.ch", username='medizin4', pkey=key)
# Open the SFTP channel
sftp = ssh.open_sftp()

# Upload the Weather Report and the Last Update DateTime jpg
sftp.put(f"{local_basepath}Brieftauben_Wetterreport.pdf", f"{remote_basepath}Brieftauben_Wetterreport.pdf")
sftp.put(f"{local_basepath}/last_update_date_time.jpg", f"{remote_basepath}last_update_date_time.jpg")

# Close the SFTP channel
sftp.close()