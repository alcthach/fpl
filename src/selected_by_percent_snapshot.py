import requests
import time 
import json
import datetime
from scraper import Scraper

# This can probably live in the Scraper class...
def get_timestamp():
    timestamp = datetime.datetime.now().isoformat()
    return timestamp

# This specific to the type of pull I'm making but maybe I can think about making this more dynamic
# So that this can live in the Scraper class as well
# There is a version of this function but it writes the name of the endpoint rather than the type of 
# Data pull that it's making

def write_to_file(data):
    with open(f"../data/selected_by_percent/selected_by_percent_daily_snapshot_{get_timestamp()}.txt", 'w') as export_file:
        json.dump(data, export_file)

def get_selected_by_pct(data):
    selected_by_pct_data = [ ] 
    for player in data:
        selected_by_pct_data.append(
                               {
                               'id' : player['id'],
                               'selected_by_percent': player['selected_by_percent'],
                               'timestamp' : get_timestamp()
                               }
                               )
    return selected_by_pct_data

# This uses an identical pattern to the transfer data pull
# However, the difference is that the Scraper object is going to be pulled at different timeframes
# Which means that once a day I'll these two functions will use the same Scraper object 

def main():
    Players = Scraper('get_bootstrap_static', 'elements')
    data = Players.data 
    selected_by_pct_data = get_selected_by_pct(data)
    write_to_file(selected_by_pct_data)

if __name__ == "__main__":
    main()

# NOTES:
# - Maybe I could think about placing some of this in the fpl_config file?
# - This might make sense because I have to make changes to the db init file as well
# - In that case maybe I could try to make that change after 


