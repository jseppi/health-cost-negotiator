import csv
import sqlite3 as sql

# Load Zip to HSA and HRR csv file from Dartmouth Atlas

with sql.connect('cmsdata.s3db') as con:
    cur = con.cursor()
    
    with open('hosp_hsa_hrr_2010.csv') as f:
        r = csv.DictReader(f)
        for row in r:

            # For each line, find the provider with provider_id
            # and set its hrr_id and hsa_id to the values in the row

            # Then create new hrr record with hrr_id and hrr_name

            # and new hsa record with hsa_id and hsa_name

            cur.execute("UPDATE providers \
                SET hrr_id=?, hsa_id=?, city=? \
                WHERE id=?", 
                (row['hrrnum'], row['hsanum'], row['hospcity'], row['provider'])
            )


            cur.execute("INSERT OR REPLACE INTO hrrs \
                (id, state, city) \
                VALUES (?, ?, ?)",
                (row['hrrnum'], row['hrrstate'], row['hrrcity'])
            )

            cur.execute("INSERT OR REPLACE INTO hsas \
                (id, state, city) \
                VALUES (?, ?, ?)",
                (row['hsanum'], row['hsastate'], row['hsacity'])
            )
            