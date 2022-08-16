"""
FPL Transfers Data Loading Script
Alex Thach - alcthach@gmail.com
2022-07-21
"""

import psycopg2
from psycopg2.extras import Json 
import json

file_to_load = "../data/data_events.txt" # Was transfers, but switched to events for testing

# Config file to pull column list and insert scripts
config_file = "fpl_config.json"
config = open(config_file)
config_data = json.load(config)



# TODO: Refactor line below into the config file, load the config file in def main(); Re: more dynamic  
# insert_script = "INSERT into transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"

def load_transfers_postgresql(file_to_load):

    conn = psycopg2.connect("dbname=fpl user=postgres") 
    cur = conn.cursor()

    transactions_sql = config_data['get_bootstrap_static']['events']['insert_script'] 

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


def load_events_postgresql(file_to_load):

    conn = psycopg2.connect("dbname=fpl user=postgres") 
    cur = conn.cursor()

    transactions_sql = config_data['get_bootstrap_static']['events']['insert_script']

    with open(file_to_load) as events:
        data = json.load(events)
        
    rows_added = 0

    

    for row in data:
        insert_data = [ ]
        raw_data = [*row.values()]
        # insert_data = tuple([*row.values()])    

        '''
        PSEUDOCODE
        if the value is not type list
            then append the value to the list of values to insert table
        other if the value is a type list
            then convert it to str
            add double quotes around it
            and append the transformed to the list of values to insert into table
        take the list of values to insert and convert it to a tuple
        pass the tuple as an argument in the cur.execute(insert statement)
        '''

        for i in raw_data:
            if type(i) not in [list, dict]:
                insert_data.append(i)
            else:
                list_to_str = str(i)
                transformed_str = list_to_str 
                insert_data.append(transformed_str)

                
        print((transactions_sql, tuple(insert_data)))
        cur.execute(transactions_sql, tuple(insert_data))
        rows_added += 1

    print(f"Added {rows_added} row to transfers table!")

    conn.commit()

    conn.close()


def main():
    load_events_postgresql(file_to_load)

if __name__ == "__main__":
    main()    
