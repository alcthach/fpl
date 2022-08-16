"""
FPL Transfers Data Loading Script
Alex Thach - alcthach@gmail.com
2022-07-21
"""

import psycopg2
import json

file_to_load = "../data/data_fpl_transfers.txt"

# TODO: Refactor line below into the config file, load the config file in def main(); Re: more dynamic  
insert_script = "INSERT into transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"

def load_postgresql(file_to_load):

    conn = psycopg2.connect("dbname=fpl user=postgres") 
    cur = conn.cursor()

    transactions_sql = insert_script

    with open(file_to_load) as transfers:
        data = json.load(transfers)
        
    rows_added = 0

    for row in data['filtered_elements']:
        insert_data = tuple([*row.values()])
        print((transactions_sql, insert_data))
        cur.execute(transactions_sql, insert_data)

        rows_added += 1

    print(f"Added {rows_added} row to transfers table!")

    conn.commit()

    conn.close()

def main():
    load_postgresql(file_to_load)

if __name__ == "__main__":
    main()    
