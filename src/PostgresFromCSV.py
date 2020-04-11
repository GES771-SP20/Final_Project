'''
PostgresFromCSV
Created on Apr 9, 2020
authors: Scott Clement, Luis Resh
GES771: Advanced Spatial Data Management

This program uses the pandas and psycopg2 libraries to: 
1. Read in a csv file from the covidtracking.com api 
2. Filter out unneeded columns, handle null values, and other data cleanup
3. Populate additional fields with values derived from the original imported values
4. Copy data to a postgres database 
'''

# imports
import pandas as pd
import numpy as np
import psycopg2
import sys
# import geopandas as gp
# import json
# import csv

''' 
loadDataframe() function
Purpose: Read in data from three separate sources and combine into a single dataframe
Required parameters: url of api
Returns: Single dataframe with processed data
'''
def loadDataframe(url):
    
    try:
        
        try:
            # Read COVID-19 time series data from api into dataframe.
            df = pd.read_csv(url, sep=",") # add usecols=[] and index_col='fieldname' parameters
            print("CSV read from url complete.")
            print(data)
    
        except:
            print("Unable to read data from {}".format(url))
            raise
        
        del df['fieldname1', 'fieldname2'] # Delete unneeded columns
        df.rename(columns={'oldName':'newName'}, inplace=True) # rename columns
        # handle null values
                 
        print("Process status: Initial dataframe {} loaded from api.\n".format(df.shape))
        print("Dataframe first 10 rows:\n\n{}\n".format(df.head(10)))
        
        return df
    
    except:
        print("Error in loadDataframe() function: {}\n".format(sys.exc_info()))
        raise

'''
addColumns() function
Purpose: Add and populate new fields... infectRate, hospRate, deathRate
Required parameter: Dataframe with original loaded data
Returns: Dataframe with additional columns populated
'''
def addColumns(df2):
    
    try: 
        # Use column operations to populate PopDensity, PopChg, and PctPopChg fields
        df2['InfectRate'] = df2['positive'] / df2['totalTestResults']
        df2['HospRate'] = df2['hospitalizedCumulative'] / df2['positive']
        df2['DeathRate'] = df2['death'] - df2['positive']

        print("Process status: Additional columns inserted and populated in dataframe {}.\n".format(df2.shape))
        print("Dataframe first 10 rows:\n\n{}\n".format(df2.head(10)))
    
        return df2
    
    except:
        print("Error in addColumns() function: {}\n".format(sys.exc_info()))
        raise

'''
exportToPostgres() function
Purpose: export dataframe to postgres database
Required parameter: Dataframe with loaded data
Returns: Dataframe with additional columns populated
'''

def exportToPostgres(df3):
    
    try:
        #establish database connection and cursor
        conn = psycopg2.connect("host=localhost dbname=postgres user=postgres") # change to actual databcase connection string
        cur = conn.cursor()
        
        # export datatable to postgres
        cur.copy_from(df3, 'tablename', sep=',')
        conn.commit()
        
        print("Process status: Postgres table updated {}.\n".format(df3.shape))
        
    except:
        print("Error in exportToPostgres() function: {}\n".format(sys.exc_info()))
        raise

##### EXECUTE PROGRAM ###############################
# Assign input and output filepath strings to variables.
urlin='https://covidtracking.com/api/v1/states/daily.csv'

# Call local functions
try:
    data = loadDataframe(urlin) # returns "cleaned" dataframe with data imported from api
    data2 = addColumns(data) # returns dataframe with additional populated columns
    exportToPostgres(data2) # updates postgres table with data from dataframe
        
except:
    print("Program terminated prior to completion.")
    sys.exit(1)
    
print("Program completed.")



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
 

