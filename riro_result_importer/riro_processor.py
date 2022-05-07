import re
from mysql import connector

# INPUT PARAMETER
zuechter = 'Hirschi Simon+Beat'
km = "189"
auflassort = "Ehingen"
flugnr = "2"
flugdatum = "2021-05-15"
# Set to False for validation/testing
db_insert = True
# input file (content copied from a sample result list from www.riro.de)
filepath = '/Users/ph/Projects/riro_result_importer/results/regv02kr02/results.txt'
# useful for validation purposes: https://regex101.com/
pattern  = '^(\s*)([1-9][0-9]*[a-z]?)(\s*)([1-9][0-9]*[a-z]?)?(\s*)([0-1][0-9]*)?(\s*)([a-zA-Z]*)?(\s*)([0-9]*)(\s*)([0-9]*)?(\s*)([0-9]*W?\s)(\s*)([a-zA-Zäöüéèß&]*[.,]?\s*[,]?\s*[a-zA-Zäöüéèß&]*\s*[,+]?[a-zA-Zäöüéèß&]*\s*[+-.\/]*\s*[a-zA-Zäöüéèß&]*.?)(\s*)([0-9][0-9])(\s*)([0-9]*\/\s*[0-9]*)?(\s*)([0-9][0-9]?\s)?(\s*)([0-9]*.[0-9]*.[0-9]*)(\s*)(-?[0-9]\s)?(\s*)([0-9]*,[0-9]*)(\s*)([0-9]*,[0-9]*)?(\s*)([0-9]*,[0-9]*)?(\s*)([A-Z])?(\s*)([0-9]*\/\s*[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*,?[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)$'


def insert_result_row(taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnr, flugdatum):
    #establishing the connection
    conn = connector.connect(user='riro_webscraper_app', password='12345', 
    host='127.0.0.1', database='brieftauben')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO 2022_Flugsaison_Hirschi(
    taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnummer, flugdatum)
    VALUES ('"""+ taubennr+"""', '"""+ prs +"""', '"""+ mmin+"""', 
    '"""+ prs_fg+"""', '"""+ prs_rv+"""', '"""+ prs_zt+"""', '"""+ prs_tb+"""', '"""+ aspkt_fg+"""'
    , '"""+ aspkt_rv+"""', '"""+ auflassort+"""', '"""+ km+"""', '"""+ flugnr+"""', '"""+ flugdatum+"""')"""

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
prs = ""
mmin = ""
prs_fg = ""
prs_rv = ""
prs_zt = ""
prs_tb = ""
aspkt_fg = ""
aspkt_rv = ""

counter = 0
# Iterate each line
for line in lines:
    # if not line.__contains__(zuechter):
    #     continue
    # Regex applied to each line 
    match = re.search(pattern, line)
    if match and match.group(16).strip() == zuechter:
        counter += 1
        if(match.group(20)):
            prs = match.group(20).strip()
            print("Preise: " + prs)

        if len(match.group(10).strip()) == 2:
            taubennr = (match.group(8).strip() or "DE") + "-" + match.group(10).strip().lstrip("0") + "-" + match.group(12).strip().lstrip("0") + match.group(14)
        else:
            taubennr = (match.group(8).strip() or "DE") + "-" + match.group(12).strip().lstrip("0") + "-" + match.group(10).strip().lstrip("0") + match.group(14)

        if match.group(28):
            mmin = match.group(28).strip()
        else: 
            mmin = ""
        if match.group(30):
            aspkt_fg = match.group(30).strip()
        else: 
            aspkt_fg = ""
        if match.group(32):
            aspkt_rv = match.group(32).strip()
        else: 
            aspkt_rv = ""
        if match.group(2):
            prs_fg = match.group(2).strip()
        else: 
            prs_fg = ""
        if match.group(4):
            prs_rv = match.group(4).strip()
        else: 
            prs_rv = ""
        if match.group(36):
            prs_tb = match.group(36).strip()
        else: 
            prs_tb = ""

        prs_zt = str(counter)
        
        if db_insert:
            insert_result_row(taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnr, flugdatum)
        print(prs_zt + ". " + taubennr + " --- " + mmin + " - " + aspkt_fg + " - " + aspkt_rv + " - " + prs)

