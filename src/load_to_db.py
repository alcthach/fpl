"""
FPL Transfers Data Loading Script
Alex Thach - alcthach@gmail.com
2022-07-21
"""

# NOTE I think out loud quite a bit in this script, however the prod script will be much cleaner!


import psycopg2
from psycopg2.extras import Json 
import json

# CAUTION THIS IS HARDCODED
# I'll have to find a way to loop through each file and also pull the corresponding insert script from
# The config file
# Possible idea: f"../data/get_bootstrap_static_{endpoint}.txt" 
    # This allows me to also reach into the same endpoint in the config file to get the corresponding
    # Insert script
# Something like for each endpoint in fpl_config.json
# Find the corresponding file in the directory
# Pull the insert script
# Also pull the correct txt file where the data lives
# The function that loads the data will need to have endpoint as a parameter as well...
# I might have to consider creating a class and initializing it with the endpoint? I'm not quite sure yet# I know that somewhere in the script I'll have to do something like for endpoints in config_data, 
# Load_to_db(endpoints)
# It's also a question if this is the most performant way of doing it, I.E. using python
# For now it's okay because it doesn't seem like that much data...
# I ran some commands in interactive Python CLI, I could initialize a class with a list of the endpoints # That are present in the config file using `[key for key in config_data['get_bootstrap_static']['endpoint']]`



"""
Notes:
- A majority of the tables that I'm looking to load to the staging layer contain multiple rows
- Only game_settings contains a single-row, total_players just contains a single value; I'll have to find a way to deal with the latter
- I tried to diagram how I'm going to approach these problems but I'm going to think through them here, and write some pseudo-code below
- I might just have a notes/scratch-pad area in my scripts for this type of stuff moving forward

Loading txt files to postgres:

- I have jsons of the endpoints that I pulled using the scraper script
- I'm now tasked with figuring out how to export these json files to the db
- So far I've been successful with the 'events' and 'game_settings' endpoints, however, I'll have to figure out the actually control flow of what is going on 

Spelling out the control flow:
Input -> json of endpoint in txt file
Output -> write each row in json to corresponding table in postgres db

- Take the json file
- Make it accessible to python 
- Basically turn it into a python dictionary
- Something to consider is that the multidimensional dicts might be lists? 
- I'll have to investigate this momentarily, brb
- The answer is yes, some of these endpoints are a list of dicts
- This means I'll have to consider the pattern I want to employ

I.E.
Input -> either dict or list of dicts
Take values from dict or each dict in the list of dicts (I.E. row)
Pass those values in an INSERT statement, cur.execute(insert statement, values)
INSERT INTO table columns, values

PSEUDOCODE:
    If input is a list of dicts,

        For dict in list:
            if value in dict is not a dict or list:
                append to transformed_insert_values list
            else 
                convert the dict or list into type str
                append to the transformed values lst
        
        Take this list and turn it into a tuple

        Pass the tuple as an argument in curr.exec() 

    else if the object is a dict

        grab the values in the dict
        place into a lst
        convert to tuple
        and pass tuple as an argument in curr.exec()

NB I don't think curr.exec() needs to be called twice as seen above...


    
     
"""

# TODO: Refactor line below into the config file, load the config file in def main(); Re: more dynamic  
# insert_script = "INSERT into transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"


def load_to_db(file_to_load, endpoint):
    # Same with the commands below, do I need to connect and init a cursor at every endpoint?
    conn = psycopg2.connect("dbname=fpl user=postgres")
    cur = conn.cursor()

    

    # This is coded generically, 'endpoint' represents the key in dict of endpoints, this is not coded
    # in fpl_config.json TODO revise fpl_config.json to reflect this 
    # Running into a possible blocker though... how do I automate it so that it cycles through all
    # endpoints? TODO 
    # 'endpoint' might have to be a variable, or gets passed through as an argument in load_to_db()
    # ENDPOINT IS HARD-CODED! TODO Make dynamic afterwards
    transactions_sql = config_data['get_bootstrap_static']['endpoints'][endpoint]['insert_script']

    # Create file object from txt file holding json, then takes file object and returns json object(dict)
    # data represents a json object
    with open(file_to_load) as endpoint:
        data = json.load(endpoint)

    # Initialize counter
    rows_added = 0 # EDIT: scoped incorrectly! see load_to_db()



    # Print type for data
    # If the object is a list, it'll just count the number of elements
    # IF the object is a dict, it'll count the number of key values pairs
    # If the object is an int, you're SOL
    print(f"Loading {file_to_load}")
    print(type(data))
    

    # Intialize insert_values list, TODO scope this properly, have it re-initialize which each endpoint
    # insert_values_lst = [ ] 


    # What I'm trying to do here is figure out if I need to iterate through the lst or if I can pull the
    # Values straight out of the object, instead of hard-coding or writing two seperate functions,
    # I can decide how I'm going to operate on the data object
    # I'll have to understand the control flow of the nested loop below
    # I.E. I need to know when my row is ready to pass as an argument, right now it's a bit unclear to me
    
    # Figure out if object is a single dict or list of dicts
    # If the object is a list of dicts, take the next dict and unpacked its values into a list
    # If the object is a list of dicts, look at each dict, and each value in the dict and convert to str if appropriate
    # Append these values to a list, will be pass as an argument for my insert script later on...
    # When the values have been inserted into the database table, re-initialize the insert_values_lst... 
    # I'll give this a try for now...
    # If the list doesn't get initialized I'm going to be thrown an index out of range error...


    # TODO When coming back to this, write if statement to check if the data object is a str
    # If yes, pass for now, I'll come back to it later!
    # Re: Just trying to debug this and see if I'm getting the outputs that I'm looking for
    # After than I will try to insert values into the db

"""
Notes
2022-08-14

- I've been experiencing some strife with the block of code below
- It's good that I aware of how it's making me feel, blocked for lack of better word
- In which case, it's made me realized that I should discard this pattern
- Reason being, the function is going to be difficult to write a test for
- And I feel bad for anyone that has to understand the control for the loops below, I mean it's a nested if loop within a nested if loop with a for loop nested in the if loop
- There's just too many layers
- Instead I'll explode this code block, writing a separate function based on what sort of data type I'm looking at :)

- PSEUDOCODE:
    for row in data:
        for element in row:
            check type, if type is in dict or lst:
                convert to str and append to insert_values
            else:
                append element to list
    convert to tuple
    return values_to_insert tuple

def load_to_db_if_dict(data):
    pull values
    for each value in lst of values:
        check type
            if type is dict or lst
                convert to str
        otherwise append to insert values list
    convert values_to_insert to tuple
    return values_to_insert

def load_to_db_if_int(data):
    return that number


def load_to_db_main(object):    
    if object is list:
        then load_to_db_if_lst()
    else if object is dict:
        then load_to_db_if_dict()
    else if object is int:
    d    then load_to_db_if_int()
    else:
        pass



"""

# REVISED CODE FOR EASIER TESTING AND READABILITY

import psycopg2
import json


def load_config(config_file):
    config = open(config_file)
    config_data = json.load(config)
    return config_data

def get_endpoints(config_data):
    endpoints = [endpoint for endpoint in config_data['get_bootstrap_static']['endpoints']]
    return endpoints

def parse_insert_script(config_data, endpoint):
    transactions_sql = config_data['get_bootstrap_static']['endpoints'][endpoint]['insert_script']
    return transactions_sql

# def setup_psycopg():
    # conn = psycopg2.connect("dbname=fpl user=postgres")
    # cur = conn.cursor()

def get_data(file_to_load, endpoint):
    with open(file_to_load) as file:
        data = json.load(file)
    return data

def convert_to_str(raw_values):
    converted_values = [ ]
    for value in raw_values:
        if type(value) not in [list, dict]:
            converted_values.append(value)
        else:
            converted_values.append(str(value))
    return tuple(converted_values)

def load_to_db_if_lst(data, endpoint):
    for row in data:
        raw_values = [*row.values()]
        values_to_insert = convert_to_str(raw_values)
    print(f"Loaded {endpoint} endpoint.")
        # cur.execute(transactions_sql, values_to_insert)

def load_to_db_if_dict(data, endpoint):
    raw_values = [*data.values()]
    values_to_insert = convert_to_str(raw_values)
    print(f"Loaded {endpoint} endpoint.")
    # cur.execute(transactions_sql, values_to_insert)

def load_to_db_if_int(data):
    pass

# Prepares data to be loaded based on input data type
def main():
    # TODO Add to def init
    conn = psycopg2.connect("dbname=fpl user=postgres")
    cur = conn.cursor()

    config_file = "fpl_config.json"
    
    # setup_psycopg()

    config_data = load_config(config_file)
    
    endpoints = get_endpoints(config_data)
    
    for endpoint in endpoints:
        file_to_load = f"../data/get_bootstrap_static_{endpoint}.txt"
        data = get_data(file_to_load, endpoint)
        transactions_sql = parse_insert_script(config_data, endpoint)
        if type(data) == dict:
            load_to_db_if_dict(data, endpoint)
        elif type(data) == list:
            load_to_db_if_lst(data, endpoint)
        elif type(data) == int:
            load_to_db_if_int(data)
        else:
            pass
    
    # Commit changes and close connection after all the data is loaded
    conn.commit()
    conn.close()
# -----------------------------------------------------------------------------

"""
    if type(data) in [list, dict]:
        if len(data) > 1:
            print("This endpoint has multiple rows")
            for i in data:
                insert_values_lst = [ ] 
                if type(i) != dict:
                    pass
                    # print(f"This object is not a dict")
                else:
                    unpacked_values_lst = [*i.values()]
                        # Create properly formatted data types, I.E. convert to str if appropriate
                    for element in unpacked_values_lst:
                        if type(element) not in [list, dict]:
                            insert_values_lst.append(element)
                        else:
                            insert_values_lst.append(str(element))

                rows_added += 1


            # print(transactions_sql, tuple(insert_values_lst))
            # cur.execute(transactions_sql, tuple(insert_values_lst))


            # Do I need the commands below to run everytime insert a new row into the table???
            # Or am I okay to commit changes and close connection after all the tables have been updated?
            # As a side-note, it would be lovely to find someone to help review my code!
            # conn.commit()
            # conn.close()


            print(f"Rows added: {rows_added}")
            print("")

    else:
        print("This endpoint has less than two rows")
        print("")

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

    # HARDCODED, TODO make dynamic
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


def load_bootstrap_game_settings(file_to_load):
    # Set up postgres adapter
    conn = psycopg2.connect("dbname=fpl user=postgres")
    cur = conn.cursor()

    # This is hard-coded, Re: Reaches into the specific key-value pair
    transactions_sql = config_data['get_bootstrap_static']['game_settings']['insert_script']

    with open(file_to_load) as game_settings:
        data = json.load(game_settings)

    rows_added = 0

    insert_data = [*data.values()]

    cur.execute(transactions_sql, insert_data) 
    conn.commit()
    conn.close()

#TODO Define new function for 'game_settings' b/c it's actually only one row, one-dimensional
#TODO Revise 'events' function back to what it was before, Re: events is a list of dictionaries...


def main():
    # load_events_postgresql(file_to_load)
    # load_bootstrap_game_settings(file_to_load)
    for endpoint in endpoints:
        rows_added = 0
        file_to_load = f"../data/get_bootstrap_static_{endpoint}.txt" 
        load_to_db(file_to_load, endpoint)
        print(f"Loaded {endpoint} to staging layer")
"""


if __name__ == "__main__":
    main()    
