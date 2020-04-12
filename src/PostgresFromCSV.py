'''
PostgresFromCSV
Created on Apr 9, 2020
authors: Scott Clement, Luis Resh
GES771: Advanced Spatial Data Management

This program uses the pandas and psycopg2 libraries to: 
1. Read select columns in a csv file from an api url into a dataframe
2. Reorder and rename columns, handle null values, other data cleanup
3. Populate additional columns with values derived from the original imported values
4. Copy processed data to a postgres database table
'''

##### IMPORTS ###########################
import pandas as pd
import numpy as np
import sys
import StringIO as sio
import psycopg2 as pg

##### LOCAL FUNCTIONS ####################
''' 
loadDataframe() function
Purpose: Read in specific data columns from a file source, re-order and rename the columns, replace NaN values
Required parameters: filepath, delimiter, column order list, rename dictionary, replacement value for NaNs
Returns: Dataframe with processed data
'''
def loadDataframe(fpath, cols=[], delim=',', rename={}, nanValue=np.NaN):
    
    try:
        
        try:
            if cols:
                df = pd.read_csv(fpath, sep=delim, usecols=cols)[cols] # Read specified column data (in list order) from file into dataframe.
            else:
                df = pd.read_csv(fpath, sep=delim) # Read in all columns from file
            print("CSV data read from url {}.".format(url))
    
        except:
            print("Unable to read data from {}".format(url))
            raise
        
        df.rename(columns=rename, inplace=True) # rename columns
        df.fillna(nanValue, inplace=True) # replace NaN with zeros
                 
        print("Process status: Dataframe {} loaded from api.\n".format(df.shape))
        print("Dataframe first 10 rows:\n\n{}\n".format(df.head(10)))
        return df
    
    except:
        print("Error in loadDataframe() function: {}\n".format(sys.exc_info()))
        raise

'''
addRateCols() function
Purpose: Add and populate new rate columns
Required parameter: Dataframe with processed data, dictionary of rates to be calculated and added as columns
Returns: Dataframe with additional columns populated
'''
def addRateCols(df, ratesDict):
    
    try: 
        # Use column operations to create and populate rate columns defined in ratesDict
        
        for key in ratesDict:
            numdenom = ratesDict.get(key)
            num = numdenom[0]
            denom = numdenom[1]
            df[key] = df[num] / df[denom]

        df.replace(to_replace = [np.nan, np.inf], value = 0, inplace=True) # replace possible divide-by-zero results with zero
        
        print("Process status: Rate columns inserted and populated in dataframe {}.\n".format(df.shape))
        print("Dataframe first 10 rows:\n\n{}\n".format(df.head(10)))
        return df
    
    except:
        print("Error in addRateCols() function: {}\n".format(sys.exc_info()))
        raise

'''
copyToPostgres() function
Purpose: Copy data in dataframe to postgres database table
Required parameters: Dataframe with processed data, db connection string, db table name
Returns: n/a
'''
def copyToPostgres(df, connectParams, tableName):
    
    print("Connecting to database " + connectParams + " table " + tableName + "...")
    
    try:
        
        conn = pg.connect(connectParams) # establish database connection
        print ("Connection to database established.")
        
        buf = sio.StringIO() # create text buffer
        df.to_csv(buf) # write dataframe to buffer
        buf.seek(0) # reset buffer position to beginning
        print("Data read into text buffer")      
        
        with conn.cursor() as cur: # with statement provides error handling and closes cursor at end of code block
            cur.execute("truncate " + tableName + ";") # clear out all existing data from db table
            cur.copy_from(buf, tableName, sep=',') # copy from buffer to postgres table
            #sqlStatement = """COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"""
            #cur.copy_expert(sql=sqlStatement % tableName, file=buf) # Alternative to copy_from method
            conn.commit()
            
            fout = open('pgCopyConfirmation.csv', 'w')
            cur.copy_to(fout, tableName, sep=",") # to confirm data loaded to the db table
                        
        print("Process status: Postgres table {} updated {}.\n".format(tableName, df.shape))
        
    except:
        print("Error in copyToPostgres() function: {}\n".format(sys.exc_info()))
        raise

    finally:
        fout.close()
        buf.close()
        cur.close() # redundant?
        conn.close()

##### EXECUTE PROGRAM ###############################

# Assign variables
url ='https://covidtracking.com/api/v1/states/daily.csv'
colsIn = ['date', 'state', 'fips', 'positive', 'negative', 'totalTestResults', 'hospitalized', 'death'] # List source column names in desired order for dataframe
colsRename = {'totalTestResults':'totalTests', 'death':'deaths'} # key is source column name, value is new column name for dataframe

# key is column name for calculated rate; value is tuple of numerator and denominator columns
ratesToCalc = {'infectRate':('positive','totalTests'), 'hospRate':('hospitalized', 'positive'), 'deathRate':('deaths', 'positive')} 

connString = 'host=localhost dbname=postgres user=postgres password=provide_password_if_needed'
dbTableName = 'TBD' # include schema.table

# Call local functions
try:
    data = loadDataframe(url, delim=',', cols=colsIn, rename=colsRename, nanValue=0) # returns "cleaned" dataframe with data imported from api
    data = addRateCols(data, ratesToCalc) # returns dataframe with additional populated rate columns
    copyToPostgres(data, connString, dbTableName) # updates postgres table with processed data from dataframe
        
except:
    print("Program terminated prior to completion.")
    sys.exit(1)
    
print("Program completed.")

##### END OF PROGRAM #################################

##### CODE SAMPLES ###################################
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
 
'''
reoderCols() function
Purpose: Reorder and move a list of dataframe columns before or after a reference column
Required parameters: dataframe, list of columns to be moved in the order they are to be placed, reference column, place relative to reference column = "before' or 'after'
Returns: dataframe with reordered columns
'''
'''
def reorderCols(df, movecols=[], refcol='', place='after'):
    
    try:
        
        cols = df.columns.tolist()
        if place == 'after':
            seg1 = cols[:list(cols).index(refcol) + 1]
            seg2 = movecols
        if place == 'before':
            seg1 = cols[:list(cols).index(refcol)]
            seg2 = movecols + [refcol]
    
        seg1 = [i for i in seg1 if i not in seg2]
        seg3 = [i for i in cols if i not in seg1 + seg2]
    
        print("Process status: Dataframe columns re-ordered.\n".format(df.shape))
        print("Dataframe first 10 rows:\n\n{}\n".format(df.head(10)))
        return(df[seg1 + seg2 + seg3])

    except:
        print("Error in reorderCols() function: {}\n".format(sys.exc_info()))
        raise
'''    
