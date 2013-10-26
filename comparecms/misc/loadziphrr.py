import csv
import sqlite3 as sql

# Load Zip to HSA and HRR csv file from Dartmouth Atlas

with sql.connect('cmsdata.s3db') as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE zip_to_hrr( \
        id int primary_key not null, \
        zip char(5), \
        hsa_id int, \
        region_id int,  \
        region_state char(2) \
        )")
    
    with open('ziphrr.csv') as f:
        r = csv.DictReader(f)
        i = 0
        for row in r:
            cur.execute("INSERT INTO zip_to_hrr \
                (id, zip, hsa_id, region_id, region_state) \
                VALUES \
                (?, ?, ?, ?, ?)", 
                (i, row['zipcode11'], row['hsanum'], 
                row['hrrnum'], row['hrrstate']))
            i = i+1
            