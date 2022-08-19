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
    with open(f"../data/player_cost_daily_snapshot_{get_timestamp()}.txt", 'w') as export_file:
        json.dump(data, export_file)

def get_player_cost_snapshot(data):
    player_cost_data = [ ] 
    for player in data:
        player_cost_data.append(
                               {
                               'id' : player['id'],
                               'player_cost': player['now_cost'],
                               'timestamp' : get_timestamp()
                               }
                               )
    return player_cost_data

# This uses an identical pattern to the transfer data pull
# However, the difference is that the Scraper object is going to be pulled at different timeframes
# Which means that once a day I'll these two functions will use the same Scraper object 

def main():
    Players = Scraper('get_bootstrap_static', 'elements')
    data = Players.data 
    player_cost_data = get_player_cost_snapshot(data)
    write_to_file(player_cost_data)

if __name__ == "__main__":
    main()

# NOTES:
# - Maybe I could think about placing some of this in the fpl_config file?
# - This might make sense because I have to make changes to the db init file as well
# - In that case maybe I could try to make that change after 


