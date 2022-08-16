"""
FPL Transfers Data Loading Script
Alex Thach - alcthach@gmail.com
2022-07-21
"""

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

def setup_psycopg():
    conn = psycopg2.connect("dbname=fpl user=postgres")
    cur = conn.cursor()

def insert_row(transactions_sql, values_to_insert):
    cur.execute(transactions_sql, values_to_insert)

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

def load_to_db_if_lst(data, endpoint, transactions_sql):
    for row in data:
        raw_values = [*row.values()]
        values_to_insert = convert_to_str(raw_values)
        conn = psycopg2.connect("dbname=fpl user=postgres")
        cur = conn.cursor()
        cur.execute(transactions_sql, values_to_insert)
        conn.commit()
        conn.close()
    print(f"Loaded {endpoint} endpoint.")

def load_to_db_if_dict(data, endpoint, transactions_sql):
    raw_values = [*data.values()]
    values_to_insert = convert_to_str(raw_values)
    conn = psycopg2.connect("dbname=fpl user=postgres")
    cur = conn.cursor()
    cur.execute(transactions_sql, values_to_insert)
    print(f"Loaded {endpoint} endpoint.")
    conn.commit()
    conn.close()

def load_to_db_if_int(data):
    pass

def main():
    config_file = "fpl_config.json"
    config_data = load_config(config_file)
    endpoints = get_endpoints(config_data)
    for endpoint in endpoints:
        file_to_load = f"../data/get_bootstrap_static_{endpoint}.txt"
        data = get_data(file_to_load, endpoint)
        transactions_sql = parse_insert_script(config_data, endpoint)
        if type(data) == dict:
            load_to_db_if_dict(data, endpoint, transactions_sql)
        elif type(data) == list:
            load_to_db_if_lst(data, endpoint, transactions_sql)
        elif type(data) == int:
            load_to_db_if_int(data)
        else:
            pass
    
if __name__ == "__main__":
    main()    
