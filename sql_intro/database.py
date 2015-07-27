import sqlite3 as lite
import pandas as pd

con = lite.connect('sql_challenge.db')

#cities to be added to db
cities = (('New York City', 'NY'),
          ('Boston', 'MA'),
          ('Chicago', 'IL'),
          ('Miami', 'FL'),
          ('Dallas', 'TX'),
          ('Seattle', 'WA'),
          ('Portland', 'OR'),
          ('San Francisco', 'CA'),
          ('Los Angeles', 'CA'),
          ('Washington', 'DC'),
          ('Houston', 'TX'),
          ('Las Vegas', 'NV'),
          ('Atlanta', 'GA'))

#weather to be added to db
#note that for the last 4 entries I made up the average_high value - these were
#mising in the course materials
weather = (('New York City', 2013, 'July', 'January', 62),
           ('Boston', 2013, 'July', 'January', 59),
           ('Chiago', 2013, 'July', 'January', 59),
           ('Miami', 2013, 'August', 'January', 84),
           ('Dallas', 2013, 'July', 'January', 77),
           ('Seattle', 2013, 'July', 'January', 61),
           ('Portland', 2013, 'July', 'Decembar', 63),
           ('San Francisco', 2013, 'September', 'December', 64),
           ('Los Angeles', 2013, 'September', 'December', 75),
           ('Washtington', 2013, 'July', 'January', 67),
           ('Houston', 2013, 'July', 'January', 88),
           ('Las Vegas', 2013, 'July', 'December',80),
           ('Atlanta', 2013, 'July', 'January',78))

with con:
    cur = con.cursor()
    #remove tables if already exist
    cur.execute("DROP TABLE IF EXISTS cities")
    cur.execute("DROP TABLE IF EXISTS weather")
    #create cities and weather tables
    cur.execute("CREATE TABLE cities (name text, state text)")
    cur.execute("CREATE TABLE weather (city text, year integer,"
                "warm_month text, cold_month text, average_high integer)")
    #insert associated info into tables
    cur.executemany("INSERT INTO cities VALUES (?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES (?,?,?,?,?)", weather)

    #make this interactive by asking user to select a month
    #months in db have first letter capitalized
    user_month = raw_input("Sort by which month: ").capitalize()
    
    #join tables and load into pandas df
    cur.execute('''SELECT name, state, year, warm_month, cold_month, average_high
                FROM cities 
                INNER JOIN weather 
                ON name = city
                WHERE warm_month = "{}"'''.format(user_month))
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)

    #get list of cities. unclear if supposed to indexing into pandas df to
    #achieve this. This seemed like a simplier way to do it. 
    cur.execute('''SELECT name, state
                FROM cities 
                INNER JOIN weather 
                ON name = city
                WHERE warm_month = "{}"'''.format(user_month))
    warmest = cur.fetchall()

    #output to user. kind of ugly
    if len(warmest) == 1:
        print("The city that is warmest in {} is: ".format(user_month) +
              "{}, {}".format(warmest[0][0], warmest[0][1]))
    elif len(warmest) > 1:
        warmest_string = ""
        for pair in warmest[:-1]:
            warmest_string += "{}, {}, ".format(pair[0], pair[1])
        warmest_string += "and {}, {}.".format(warmest[-1][0], warmest[-1][1])

        print("The cities that are warmest in {} are: ".format(user_month) +
              warmest_string)
    else:
        print("No cities have {} as their warmest month.".format(user_month))




