import pandas as pd
from sqlalchemy import create_engine
import pymysql

def get_fluege(tablename):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT DISTINCT flugdatum, CAST(flugnummer AS UNSIGNED) AS flugnummer, auflassort, km, prs FROM brieftauben.`" +tablename+ "`"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close()

def get_agg_resultate(tablename, tablename_eingesetzt):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT  EING.taubennr, \
                    CAST(SUM(IF(CHAR_LENGTH(RESULTATE.prs_fg)>0,1,0)) AS UNSIGNED) AS prs_fg, \
                    CAST(SUM(IF(CHAR_LENGTH(RESULTATE.prs_rv)>0,1,0)) AS UNSIGNED) AS prs_rv, \
                    COALESCE(SUM(CAST(REPLACE(RESULTATE.aspkt_fg,',','.') AS DECIMAL(4,2))),0) AS aspkt_fg_total, \
                    COALESCE(SUM(CAST(REPLACE(RESULTATE.aspkt_rv,',','.') AS DECIMAL(4,2))),0) AS aspkt_rv_total \
            FROM brieftauben.`"+tablename_eingesetzt+"` 	AS EING \
            LEFT JOIN brieftauben.`"+tablename+"`	AS RESULTATE ON RESULTATE.taubennr = EING.taubennr AND RESULTATE.flugnummer = EING.flugnummer  \
            GROUP BY EING.taubennr"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close()

def get_resultate(tablename, tablename_eingesetzt):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT   EING.taubennr, \
         CAST(EING.flugnummer AS UNSIGNED) AS flugnummer, \
         RESULTATE.prs_fg,  \
         RESULTATE.prs_rv,  \
         RESULTATE.prs_zt,  \
         IF(RESULTATE.aspkt_fg IS NULL OR RESULTATE.aspkt_fg='',0,CAST(REPLACE(RESULTATE.aspkt_fg,',','.') AS DECIMAL(4,2))) AS aspkt_fg,  \
         IF(RESULTATE.aspkt_rv IS NULL OR RESULTATE.aspkt_rv='',0,CAST(REPLACE(RESULTATE.aspkt_rv,',','.') AS DECIMAL(4,2))) AS aspkt_rv  \
            FROM brieftauben.`"+tablename_eingesetzt+"` 	AS EING \
            LEFT JOIN brieftauben.`"+tablename+"`	AS RESULTATE ON RESULTATE.taubennr = EING.taubennr AND RESULTATE.flugnummer = EING.flugnummer"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close() 

def get_max_flug(tablename_eingesetzt):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT   max(CAST(flugnummer AS UNSIGNED)) AS max_flug \
            FROM brieftauben.`"+tablename_eingesetzt+"` 	AS RESULTATE"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close()
 