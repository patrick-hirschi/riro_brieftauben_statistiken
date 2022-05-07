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

def get_agg_resultate(tablename):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT  taubennr, \
                    SUM(IF(CHAR_LENGTH(prs_fg)>0,1,0)) AS prs_fg, \
                    SUM(IF(CHAR_LENGTH(prs_rv)>0,1,0)) AS prs_rv, \
                    SUM(CAST(REPLACE(aspkt_fg,',','.') AS DECIMAL(4,2))) AS aspkt_fg_total, \
                    SUM(CAST(REPLACE(aspkt_rv,',','.') AS DECIMAL(4,2))) AS aspkt_rv_total \
            FROM brieftauben.`"+tablename+"` 	AS RESULTATE \
            GROUP BY taubennr"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close()

def get_resultate(tablename):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT   taubennr, \
                    CAST(flugnummer AS UNSIGNED) AS flugnummer, \
                    prs_fg, \
                    prs_rv, \
                    IF(aspkt_fg IS NULL OR aspkt_fg='',NULL,CAST(REPLACE(aspkt_fg,',','.') AS DECIMAL(4,2))) AS aspkt_fg, \
                    IF(aspkt_rv IS NULL OR aspkt_rv='',NULL,CAST(REPLACE(aspkt_rv,',','.') AS DECIMAL(4,2))) AS aspkt_rv \
            FROM brieftauben.`"+tablename+"` 	AS RESULTATE"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close() 

def get_max_flug(tablename):
    #establishing the connection
    sqlEngine = create_engine('mysql+pymysql://riro_webscraper_app:12345@127.0.0.1:3306/brieftauben', pool_recycle=3600)
    conn = sqlEngine.connect()

    # Preparing SQL query to INSERT a record into the database.
    sql = "SELECT   max(CAST(flugnummer AS UNSIGNED)) AS max_flug \
            FROM brieftauben.`"+tablename+"` 	AS RESULTATE"

    try:
        # Executing the SQL command
        result_dataFrame = pd.read_sql(sql,conn)

        return result_dataFrame

    except Exception as e:
        print(e)

    finally:
        # Closing the connection
        conn.close()
 