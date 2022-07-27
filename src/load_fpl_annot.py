"""

Annotated Version of LOAD script
Purpose: To review the code and understand the control flow 
Alex Thach - alcthach@gmail.com
2022-07-20

"""


import psycopg2
import json

# Assigning file to load as a variable, this keeps it dynamic and also makes it easier to write code
file_to_load = "../data/data_fpl_transfers.txt"


# This is going to be hard-coded for now, but I will write this to a config file after
# This is a list of the field names, these are the same as the keys in the dictionary
# TODO: Refactor into config file, then pull from config file after... CORRECTION: I don't think I need this one, unless it helps make it more dynamic...i
col_list = ['id',
            'first_name',
            'second_name',
            'selected_by_percent',
            'transfers_in',
            'transfers_out',
            'request_ts']

######################################################################################################

"""
- This is the SQL insert script that I'm going to use
- It's going to insert whatever values that I point to
- WTFFF the problem was that is was supposed (%s, %s, %s, %s, %s, %,s, %s) instead of (%s) - 2022-07-19
- It looks like '%s' is a specific operator, in this case it functions as a placeholder, where you pass the values in the second argument
- In the code below, I have the first argument which is just the insert statement
- The amount of placeholders has to much the amount of fields that I'm looking to INSERT into
"""

insert_script = "INSERT into transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"


"""
Translated into SQL:
INSERT INTO transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts)
VALUES (%s, %s, %s, %s, %s, %s, %s)
^ Represents each player, this is dynamic; that way I can loop through each element in the JSON file and add to the table
"""


################################################################################

# Not sure what this actually does, I think it might be b/c of the data that Ben was using, "'" is a special character in SQL so we need to break it up
# It's not too important to understand right now, I'm better off looking at what's critical for my project
# Not entirely sure if this is needed either...
# def clean_string(row, schema):
#     return_string = ""
#     for column_name in schema:
#         if column_name in row:
#             clean_string + str(row[column_name].replace("'", "\\'"))
#         else:@
#             clean_string = ""
#         return_string = return_string + "'" + str(clean_string) + "',"8

################################################################################

"""
- This is a very important function
- But I need to know how this actual works

PSEUDOCODE VERSION 
function load_to_DB takes json file:
    establishes connection to db
    instantiate cursor instance to interact with db
    assigns transaction_sql to insert_script; N.B. this is one argument that needs to be passed, still need values as well
    with statement for exception handling, instantiate file object from file transfers
        return json object object from file object, store as variable called data

    loop through each element in the list of players, note, the list is couple with key name 'filtered_elements'
        insert_data -> take the values of each element, which is a dict, return as a list, then convert to a tuple, b/c we require the values to insert to be a tuple...
        print the complete SQL statement just to see if it's correct, I.E. INSERT statement and the values that I'm looking to load into the table
        then I execute the SQL statement, passing the insert statement as one argument, and the values as another
        loop ends when I have written all the players' data in 'filtered_elements' to the table

    commit the changes to the table by calling cur.commit()
    
    close the connect to the table, Re: don't need to be connected to the db anymore


"""

def load_postgresql(file_to_load): # takes my json file as a parameter
    conn = psycopg2.connect("dbname=fpl user=postgres password=root") 
    cur = conn.cursor()
    # Hard-coding, can revise after
    transactions_sql = insert_script
    with open(file_to_load) as transfers:
        data = json.load(transfers)
    # schema = col_list #TODO Can be deleted, I think Re: Schema is already set in the commented-out statement below
    # Ran through CLI once

    # cur.execute("CREATE TABLE transfers (id integer, first_name varchar, second_name varchar, selected_by_percent float, transfers_in integer, transfers_out integer, request_ts timestamp);")


    for row in data['filtered_elements']:
        # insert_data= ""
        insert_data = tuple([*row.values()])
        # insert_data = insert_data[:-1] 
        # sql_string = transactions_sql, insert_data
        print((transactions_sql, insert_data))
        cur.execute(transactions_sql, insert_data) # This actually takes two arguments, a string and a tuple, I.E. insert statement, and values to input
        # I didn't see this so I was trying a bunch of stuff from

        # Looks like I need to pass the INSERT statement as (string, tuple)
        # I.E. (INSERT statement, values)

    conn.commit()

    conn.close()
        
# TODO Each element in the list is a dictionary, call element.values() to pull just the values in the element


def main():
    load_postgresql(file_to_load)

if __name__ == "__main__":
    main()

# TODO, fix the JSON so that it doesn't have the header... I think that this might be throwing it off a bit not needed