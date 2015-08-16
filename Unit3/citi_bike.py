import time
import requests
import collections
import sqlite3 as lite
from pandas.io.json import json_normalize
from dateutil.parser import parse

r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike.db')
cur = con.cursor()

#create reference table
with con:
    #cur.execute("DROP TABLE IF EXISTS citibike_reference")
    cur.execute('''CREATE TABLE citibike_reference
    (id INT PRIMARY KEY,
    totalDocks INT,
    city TEXT,
    altitude INT,
    stAddress2 TEXT,
    longitude NUMERIC,
    postalCode TEXT,
    testStation TEXT,
    stAddress1 TEXT,
    stationName TEXT,
    landMark TEXT,
    latitude NUMERIC,
    location TEXT )''')

#a prepared SQL statement we're going to execute over and over again
sql = """INSERT INTO citibike_reference 
      (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, 
       testStation, stAddress1, stationName, landMark, latitude, location) 
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""

#for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        #(id, totalDocks, city, altitude, stAddress2, longitude, postalCode,
        #testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,
	(station['id'],
	station['totalDocks'],
	station['city'],
	station['altitude'],
	station['stAddress2'],
	station['longitude'],
	station['postalCode'],
	station['testStation'],
	station['stAddress1'],
	station['stationName'],
	station['landMark'],
	station['latitude'],
	station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids] 

#create available_bikes tabble
#in this case, we're concatentating the string and joining all the station ids
#(now with '_' and 'INT' added)
with con:
    #cur.execute("DROP TABLE IF EXISTS available_bikes")
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +
                ", ".join(station_ids) + ");")


def _add_available(r=r, con=con, cur=cur):
    """
    Update available_bikes table with execution time and value for available
    bikes at each station (-id) for current request
    """
    #take the string and parse it into a Python datetime object
    exec_time = parse(r.json()['executionTime'])

    #add entry for execution time to db
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)',
                    (exec_time.strftime('%s'),))

    #defaultdict to store available bikes by station
    id_bikes = collections.defaultdict(int) 

    #loop through the stations in the station list
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    #iterate through the defaultdict to update the values in the database
    with con:
        for k, v in id_bikes.iteritems():
            cur.execute("UPDATE available_bikes SET _" + str(k) + " = " +
                        str(v) + " WHERE execution_time = " +
                        exec_time.strftime('%s') + ";")
        
#initial call to _add_available will add values for first time point, which is
#also when we generate the reference table
_add_available()

#wait 1 minute
time.sleep(60)

#want to repeat adding values for available bikes 59 more times, for 1hr total
for i in range(59):
     new_r = requests.get('http://www.citibikenyc.com/stations/json')
     _add_available(r=new_r)
     time.sleep(60)

con.close()
