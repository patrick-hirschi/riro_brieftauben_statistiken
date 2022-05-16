import re
from mysql import connector

# INPUT PARAMETER
zuechter = 'Hirschi Simon+Beat'
km = ""
auflassort = ""
flugnr = "3"
flugdatum = "2022-05-21"
anz_ztr_fg = ""
anz_ztr_rv = ""
anz_ztr_rg = ""
anz_tbn_fg = ""
anz_tbn_rv = ""
anz_tbn_rg = ""
# Set to False for validation/testing
db_insert = False
# input file (content copied from a sample result list from www.riro.de)
filepath = '/Users/ph/Projects/riro_result_importer/results/regv02kr02/results.txt'
# useful for validation purposes: https://regex101.com/
# pattern  = '^(\s*)([1-9][0-9]*[a-z]?)(\s*)([1-9][0-9]*[a-z]?)?(\s*)([0-1][0-9]*)?(\s*)([a-zA-Z]*)?(\s*)([0-9]*)(\s*)([0-9]*)?(\s*)([0-9]*W?\s)(\s*)([a-zA-Zäöüéèß&]*[.,]?\s*[,]?\s*[a-zA-Zäöüéèß&]*\s*[,+]?[a-zA-Zäöüéèß&]*\s*[+-.\/]*\s*[a-zA-Zäöüéèß&]*.?)(\s*)([0-9][0-9])(\s*)([0-9]*\/\s*[0-9]*)?(\s*)([0-9][0-9]?\s)?(\s*)([0-9]*.[0-9]*.[0-9]*)(\s*)(-?[0-9]\s)?(\s*)([0-9]*,[0-9]*)(\s*)([0-9]*,[0-9]*)?(\s*)([0-9]*,[0-9]*)?(\s*)([A-Z])?(\s*)([0-9]*\/\s*[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*,?[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)$'
pattern  = '^(\s*)([1-9][0-9]*[a-z]?)(\s*)([1-9][0-9]*[a-z]?)?(\s*)([1-9][0-9]*[a-z]?)?(\s*)([0-9][A-Z][0-9]\/)?(\s*)([0-1][0-9]*)?(\s*)([0-9]*)?(\s*)([0-9]*)?(\s*)([a-zA-Z]*)?(\s*)([0-9]*)(\s*)([0-9]*)?(\s*)([0-9]*W?\s)(\s*)([a-zA-Zäöüéèß&]*[.,]?\s*[,]?\s*[a-zA-Zäöüéèß&]*\s*[,+]?[a-zA-Zäöüéèß&]*\s*[+-.\/]*\s*[a-zA-Zäöüéèß&]*.?)(\s*)([0-9][0-9])(\s*)([0-9]*\/\s*[0-9]*)?(\s*)([0-9][0-9]?\s)?(\s*)([0-9][0-9]?\s)?(\s*)([0-9]*.[0-9]*.[0-9]*)(\s*)(-?[0-9]\s)?(\s*)([0-9]*,[0-9]*)(\s*)([0-9]*,[0-9]*)?(\s*)([0-9]*,[0-9]*)?(\s*)([0-9]*,[0-9]*)?(\s*)([A-Z])?(\s*)([0-9]*\/\s*[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*,?[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)$'

def insert_result_row(taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnr, flugdatum, anz_ztr_fg, anz_ztr_rv, anz_tbn_fg, anz_tbn_rv, anz_tbn_rg, prs_rg, aspkt_rg, anz_ztr_rg):
    #establishing the connection
    conn = connector.connect(user='riro_webscraper_app', password='12345', 
    host='127.0.0.1', database='brieftauben')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO 2022_Flugsaison_Hirschi(
    taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnummer, flugdatum, anz_ztr_fg, anz_ztr_rv, anz_tbn_fg, anz_tbn_rv, anz_tbn_rg, prs_rg, aspkt_rg, anz_ztr_rg)
    VALUES ('"""+ taubennr+"""', '"""+ prs +"""', '"""+ mmin+"""', 
    '"""+ prs_fg+"""', '"""+ prs_rv+"""', '"""+ prs_zt+"""', '"""+ prs_tb+"""', '"""+ aspkt_fg+"""'
    , '"""+ aspkt_rv+"""', '"""+ auflassort+"""', '"""+ km+"""', '"""+ flugnr+"""', '"""+ flugdatum+"""'
    , '"""+ anz_ztr_fg+"""', '"""+ anz_ztr_rv+"""', '"""+ anz_tbn_fg+"""', '"""+ anz_tbn_rv+"""'
    , '"""+ anz_tbn_rg+"""', '"""+ prs_rg+"""', '"""+ aspkt_rg+"""', '"""+ anz_ztr_rg+"""')"""

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
prs_rg = ""
prs_fg = ""
prs_rv = ""
prs_zt = ""
prs_tb = ""
aspkt_fg = ""
aspkt_rv = ""
aspkt_rg = ""

counter = 0
# Iterate each line
for line in lines:
    # if not line.__contains__(zuechter):
    #     continue
    # Regex applied to each line 
    match = re.search(pattern, line)
    if match and match.group(24).strip() == zuechter:
        counter += 1
        if(match.group(28)):
            prs = match.group(28).strip()
            print("Preise: " + prs)

        if len(match.group(18).strip()) == 2:
            taubennr = (match.group(16).strip() or "D") + "-" + match.group(18).strip().lstrip("0") + "-" + match.group(20).strip().lstrip("0") + match.group(22).strip()
        else:
            taubennr = (match.group(16).strip() or "D") + "-" + match.group(20).strip().lstrip("0") + "-" + match.group(18).strip().lstrip("0") + match.group(22).strip()

        if match.group(38):
            mmin = match.group(38).strip()
        else: 
            mmin = ""

        if match.group(44):
            if match.group(40):
                aspkt_rg = match.group(40).strip()
            else: 
                aspkt_fg = ""
            if match.group(42):
                aspkt_fg = match.group(42).strip()
            else: 
                aspkt_fg = ""
            if match.group(44):
                aspkt_rv = match.group(44).strip()
            else: 
                aspkt_rv = ""
        else:
            if match.group(42):
                if match.group(40):
                    aspkt_fg = match.group(40).strip()
                else: 
                    aspkt_fg = ""
                if match.group(42):
                    aspkt_rv = match.group(42).strip()
                else: 
                    aspkt_rv = ""
                aspkt_rg = ""
            else:
                if match.group(40):
                    aspkt_fg = match.group(40).strip()
                else: 
                    aspkt_fg = ""
                aspkt_rg = ""
                aspkt_rv = ""

        if match.group(6):        
            if match.group(2):
                prs_rg = match.group(2).strip()
            else: 
                prs_rg = ""
            if match.group(4):
                prs_fg = match.group(4).strip()
            else: 
                prs_fg = ""
            if match.group(6):
                prs_rv = match.group(6).strip()
            else: 
                prs_rv = ""
        else:
            if match.group(4):
                if match.group(2):
                    prs_fg = match.group(2).strip()
                else: 
                    prs_fg = ""
                if match.group(4):
                    prs_rv = match.group(4).strip()
                else: 
                    prs_rv = ""
                prs_rg = ""
            else:
                if match.group(2):
                    prs_fg = match.group(2).strip()
                else: 
                    prs_fg = ""
                prs_rg = ""
                prs_rv = ""

        if match.group(48):
            prs_tb = match.group(48).strip()
        else: 
            prs_tb = ""

        prs_zt = str(counter)
        
        if db_insert:
            insert_result_row(taubennr, prs, mmin, prs_fg, prs_rv, prs_zt, prs_tb, aspkt_fg, aspkt_rv, auflassort, km, flugnr, flugdatum, anz_ztr_fg, anz_ztr_rv, anz_tbn_fg, anz_tbn_rv, anz_tbn_rg, prs_rg, aspkt_rg, anz_ztr_rg)
        print(prs_zt + ". " + taubennr + " --- " + mmin + " - " + prs_fg + "/" + prs_rv + "/" + prs_rg + "-" + aspkt_fg + " - " + aspkt_rv + " - " + aspkt_rg + " - " + prs)

