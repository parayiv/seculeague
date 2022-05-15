from models import db, qradar
from sqlalchemy import func

#last_updated
max_last_updated=db.session.query(func.min(qradar.last_updated)).scalar()

def qrminussl():
    res = db.session.execute("SELECT EXISTS (SELECT 1 FROM QrMinusSl)").scalar()

    if res == 0:
        #db.session.execute("DELETE FROM QrMinusSl WHERE id!=0")
        db.session.execute("INSERT INTO SLeagueDB.QrMinusSl (qr_id, name, TYPE, enabled, owner, identifier, origin,creation_date, modification_date) SELECT q.qr_id, q.name, q.TYPE, q.enabled, q.owner, q.identifier, q.origin,q.creation_date, q.modification_date  \
                        FROM SLeagueDB.qradar q \
                        LEFT JOIN SLeagueDB.Seculeague s ON (q.name=s.name) WHERE s.name is NULL")

        db.session.execute("SELECT @n:=0")
        db.session.execute("UPDATE QrMinusSl SET id = @n := @n + 1")
        db.session.commit()
        db.session.close()
    else:
        db.session.execute("DELETE FROM QrMinusSl WHERE id!=0")
        db.session.execute("INSERT IGNORE INTO SLeagueDB.QrMinusSl (qr_id, name, TYPE, enabled, owner, identifier, origin,creation_date, modification_date) SELECT q.qr_id, q.name, q.TYPE, q.enabled, q.owner, q.identifier, q.origin,q.creation_date, q.modification_date  \
                        FROM SLeagueDB.qradar as q \
                        WHERE q.name NOT IN (SELECT name FROM SLeagueDB.Seculeague) \
                        AND q.name NOT IN (SELECT name FROM SLeagueDB.Rmvd)")
        db.session.execute("SELECT @n:=0")
        db.session.execute("UPDATE QrMinusSl SET id = @n := @n + 1")
        db.session.commit()
        db.session.close()

def slminusqr():
    db.session.execute("DELETE FROM SlMinusQr WHERE id!=0")
    db.session.execute("INSERT IGNORE INTO SLeagueDB.SlMinusQr (qr_id, name, TYPE, enabled, owner, identifier, origin,creation_date, modification_date) SELECT s.qr_id, s.name, s.TYPE, s.enabled, s.owner, s.identifier, s.origin, s.creation_date, s.modification_date  \
                    FROM SLeagueDB.Seculeague as s \
                    WHERE s.name NOT IN (SELECT name FROM SLeagueDB.qradar) \
                    AND s.name NOT IN (SELECT name FROM SLeagueDB.News)")
                   # AND s.name NOT IN (SELECT name FROM SLeagueDB.Rmvd)")
    db.session.execute("SELECT @n:=0")
    db.session.execute("UPDATE SlMinusQr SET id = @n := @n + 1")
    db.session.commit()
    db.session.close()

def newsUpdateID():
    db.session.execute("SELECT @n:=0")
    db.session.execute("UPDATE SLeagueDB.Seculeague SET id = @n := @n + 1")
    db.session.commit()
    db.session.close()


def pulldb():
    import requests
    import mysql.connector
    import pandas
    from time import sleep
    from datetime import datetime

    #added for warning messages that shows
    #hide them because they are annoying
    from urllib3.exceptions import InsecureRequestWarning
    # Suppress only the single warning from urllib3 needed.
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    #connecting with the QRADAR API
    SEC_TOKEN = 'c971d442-6f7e-437e-b2cf-2524937e91d3'
    URL = 'https://172.16.100.30/api/analytics/rules'
    header = {
        'SEC':SEC_TOKEN,
        'Content-Type':'application/json',
        'accept':'application/json'
    }

    r = requests.get(URL, headers=header, verify=False)



    myCon = mysql.connector.connect( host='localhost', user='root', passwd='', unix_socket="/run/mysqld/mysqld.sock" )
    cur = myCon.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS SLeagueDB")
    cur.execute("USE SLeagueDB")
    cur.execute("CREATE TABLE IF NOT EXISTS qradar(id INTEGER AUTOINCREMENT,\
                                                    qr_id INTEGER PRIMARY KEY, \
                                                    name VARCHAR(200) NOT NULL UNIQUE, \
                                                    TYPE VARCHAR(10), \
                                                    enabled VARCHAR(20), \
                                                    owner VARCHAR(50), \
                                                    identifier VARCHAR(100), \
                                                    origin VARCHAR(100), \
                                                    creation_date DATETIME, \
                                                    modification_date DATETIME, \
                                                    last_updated DATETIME)")

    for rule in r.json():
        #print(rule)
        qr_id=rule['id']
        name=rule['name']
        enabled=rule['enabled']
        owner=rule['owner']
        identifier=rule['identifier']
        origin=rule['origin']
        creation_date=datetime.fromtimestamp(int(rule['creation_date']) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        modification_date=datetime.fromtimestamp(int(rule['modification_date']) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M")
        TYPE=rule['type']

        #cur = myCon.cursor()
        sql = "INSERT IGNORE INTO qradar ( qr_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date, last_updated) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vals= (qr_id, name, TYPE,  enabled, owner, identifier, origin, creation_date, modification_date, last_updated)
        cur.execute(sql, vals)
        myCon.commit()



 