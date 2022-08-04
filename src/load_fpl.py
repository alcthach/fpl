import psycopg2
import json

# This is the file I'm looking to load...
file_to_load = "../data/data_fpl_transfers.txt"


# This is going to be hard-coded for now, but I will write this to a config file after
# This is a list of the field names, these are the same as the keys in the dictionary
col_list = ['id',
            'first_name',
            'second_name',
            'selected_by_percent',
            'transfers_in',
            'transfers_out',
            'request_ts']

# This is the SQL insert script that I'm going to use
# It's going to insert whatever values that I point to
# WTFFF the problem was that is was supposed (%s, %s, %s, %s, %s, %,s, %s) instead of (%s)
insert_script = "INSERT into transfers (id, first_name, second_name, selected_by_percent, transfers_in, transfers_out, request_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# Not sure what this actually does
# Not entirely sure if this is needed either...
# def clean_string(row, schema):
#     return_string = ""
#     for column_name in schema:
#         if column_name in row:
#             clean_string + str(row[column_name].replace("'", "\\'"))
#         else:@
#             clean_string = ""
#         return_string = return_string + "'" + str(clean_string) + "',"


# This is a very important function
# But I need to know how this actual works
def load_postgresql(file_to_load): # takes my json file as a parameter
    conn = psycopg2.connect("dbname=fpl user=postgres password=root") 
    cur = conn.cursor()
    # Hard-coding, can revise after
    transactions_sql = insert_script
    with open(file_to_load) as transfers:
        data = json.load(transfers)
    schema = col_list

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

# TODO, fix the JSON so that it doesn't have the header... I think that this might be throwing it off a bit