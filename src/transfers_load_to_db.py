# Creating a separate module to load transfers snapshot
# Alex Thach - alcthach@gmail.com
# 2022-08-21


import psycopg2
import json
import load_to_db as ldb
import os 

# Open a connection to the fpl db and instantiate a cursor


# FOR THE CONTROL FLOW BELOW, LOOP THROUGH EACH FILE
# Something like for each file in tranfers directory, if file has
# transfers_snapshot in the name, then go on and open the file and go on to 
# load the contents onto the db


# LOADING CONFIG FILE
config_file = "fpl_config.json"
config_data = ldb.load_config(config_file)
endpoint = None


# Cannot import parse_script from ldb, due to statically-coded 'endpoint'
# indexing

def parse_insert_script(config_data, snapshot_type):
    transactions_sql = config_data['get_bootstrap_static']['snapshots'][snapshot_type]['insert_script']
    return transactions_sql

transactions_sql = parse_insert_script(config_data, snapshot_type='transfers_bihourly') 

print(transactions_sql)

# For a single file... needs to stay dynamic in order to iterate through the
# directory
file_name= ""
directory = ""

files_to_load_lst = []

# file_to_load = f"home/alext/data/transfers/{file}"

for file_name in os.listdir('/home/alext/data/transfers'):
    files_to_load_lst.append(file_name)

# print(files_to_load_lst[0])


# NOTE File path is hard-coded here, just looking to make sure that I have the 
# correct object

# print(type(ldb.get_data(f"/home/alext/data/transfers/{files_to_load_lst[0]}", endpoint=None)))

data = ldb.get_data(f"/home/alext/data/transfers/{files_to_load_lst[0]}", endpoint=None)

# Double-checking to see if the dimensions of the tuple is correct
# Not correct due to governance issues, my older pulls do not have the 
# 'in_events' and 'out_events' 
# if expecting a a tuple of a certain size I'm in trouble then
# Easy way out is going to be to hard-code or move the files that I can't use 
# for now

# TODO move the older transfer pulls for now!
print(data[0])

# TRYING TO LOAD THE DATA HERE EVENTUALLY
# ldb.load_to_db_if_lst(data=data, endpoint=None, transactions_sql=transactions_sql)

# Create a file object from a single transfer data .txt file

# json.loads() - I.E. dump the contents into a json object

# Write each row of the json object or dict into the transfers_snapshot table

# Commit the changes and close the connection

# SUMMARY:
# Looks like it should be Gucci from here
# Running into a governance issue with the txt files not being consistent
# Other than that should function well


"""
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
"""
