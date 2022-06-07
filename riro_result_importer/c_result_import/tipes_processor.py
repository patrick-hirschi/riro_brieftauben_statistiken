import re
from mysql import connector

flugnr = "5"
tablename = "2022_Eingesetzte_Tauben_Hirschi"
# Set to False for validation/testing
db_insert = False
# input file (output from TIPES device)
filepath = '/Users/ph/Projects/riro/riro_brieftauben_statistiken/riro_result_importer/tipes/hirschi/202205.d00'
# useful for validation purposes: https://regex101.com/
pattern  = '^([0-9][0-9][0-9][0-9])([1-9][0-9])([A-Z][A-Z]?)\s*(0*)([1-9][0-9]*w?)\s*([0-9]*)\s*([0-9A-Z]*)(\*)([0-9]*;)([A-Z][A-Z]?)([0-9]*).([1-9][0-9]).([0-9]*w?);([a-zA-Z0-9.]*)$'

def insert_pigeon_row(taubennr, flugnr):
    #establishing the connection
    conn = connector.connect(user='riro_webscraper_app', password='12345', 
    host='127.0.0.1', database='brieftauben')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO """+ tablename + """(taubennr, flugnummer) VALUES ('"""+ taubennr+"""', '"""+ flugnr+"""')"""

    try:
        # Executing the SQL command
        cursor.execute(sql)

        # Commit your changes in the database
        conn.commit()

    except:
        # Rolling back in case of error
        conn.rollback()

    finally:
        # Closing the connection
        conn.close()

# Make sure file gets closed after being iterated
with open(filepath, 'r') as f:
   # Read the file contents and generate a list with each line
   lines = f.readlines()

taubennr = ""

counter = 0
# Iterate each line
for line in lines:
    match = re.search(pattern, line)
    if match:
        counter += 1
        
        if len(match.group(10).strip()) == 2:
            if match.group(11).strip().endswith("0"):
                taubennr = match.group(10).strip() + "-" + match.group(12).strip() + "-" + match.group(11).strip().lstrip("0") + match.group(13).strip().lstrip("0") 
            else:
                taubennr = match.group(10).strip() + "-" + match.group(12).strip() + "-" + match.group(11).strip().lstrip("0") + match.group(13).strip()
        else:
            taubennr = match.group(10).strip() + "-" + match.group(12).strip() + "-" + match.group(11).strip() + match.group(13).strip()

        nummer = str(counter)
        
        if db_insert:
            insert_pigeon_row(taubennr, flugnr)
        print(nummer + ". " + taubennr + " --- " + flugnr)
