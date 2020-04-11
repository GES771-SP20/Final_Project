'''
PostgresFromCSV
Created on Apr 9, 2020
authors: Scott Clement, Luis Resh
GES771: Advanced Spatial Data Management
'''

# imports
import pandas as pd
import psycopg2
# import geopandas as gp
# import json
# import csv

##### STATES ###############################

# read in CSV data from covidtracking api; join with state polygons in table
url='https://covidtracking.com/api/v1/states/daily.csv'
data = pd.read_csv(url, sep=",")
print("CSV read complete.")
print(data)
#data.describe()

# use pandas to filter out unneeded data; handle nulls and other data cleanup


# add columns and populate with calculated values for infection rates, hospitalization rates, and death rates

'''
# export datatable to postgres
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = conn.cursor()
with open('filename.csv', 'r') as f:
    next(f) # Skip header row.
    cur.copy_from(f, 'users', sep=',')
conn.commit()
'''
''' Alternative to wholesale copy
with open('filename.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip header row.
    for row in reader:
        cur.execute(
            "INSERT INTO users VALUES (%s, %s, %s, %s)",
            row
        )
conn.commit()
'''
##### COUNTIES ############################
 


