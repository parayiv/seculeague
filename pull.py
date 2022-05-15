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
                                                modification_date DATETIME )")

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
    TYPE=rule['type']

    #cur = myCon.cursor()
    sql = "INSERT INTO qradar ( qr_id, name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date) \
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals= (qr_id, name, TYPE,  enabled, owner, identifier, origin, creation_date, modification_date)
    cur.execute(sql, vals)
    myCon.commit()
