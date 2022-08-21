# Creating a separate module to load transfers snapshot
# Alex Thach - alcthach@gmail.com
# 2022-08-21

"""
Notes:
- I'm going to need to figure out the flow of this
- For one, I need to reach into the 'data' directory to pull the .txt file
- How much of load_to_db.py can I use?
- It might be helpful for me to import load_to_db.py as a module so that I 
  don't have to repeat myself
- It might even function better as a Class maybe? 
- Let's get it working first
- Not even sure if I might require a separate module for the initial load
  either

Pseudocode:
Pull the file
Turn into a dictionary object
Take each row in the dictionary and write to the database
"""

import psycopg2
import json
import load_to_db as ldb

def main():
    config_file = "fpl_config.json"
    config_data = ldb.load_config(config_file)
    endpoint = None
    # File is hard-coded for now, TODO: Convert so it parses for newest file
    # May require some str manipulation, and datetime?
    file_to_load = "../data/transfers/transfers_hourly_snapshot_2022-08-21T09:59:10.701023.txt"
    data = ldb.get_data(file_to_load, endpoint)
    # Hard-coded insert statement below
    transactions_sql = config_data['get_bootstrap_static']['snapshots']['transfers_hourly']['insert_script'] 
    ldb.load_to_db_if_lst(data, endpoint, transactions_sql)


if __name__ == "__main__": 
    main()
