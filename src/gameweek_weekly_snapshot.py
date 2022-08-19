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

# NOTES: 
# This one is going to be different because I'm pulling the entire data from the 'elements' endpoint
# Which means all I have to do is instantiate the Scraper class and pass 'elements' 
# Dump the data into a .txt and I'll be done


def write_to_file(data):
    with open(f"../data/gameweek_weekly_snapshot_{get_timestamp()}.txt", 'w') as export_file:
        json.dump(data, export_file)

# This uses an identical pattern to the transfer data pull
# However, the difference is that the Scraper object is going to be pulled at different timeframes
# Which means that once a day I'll these two functions will use the same Scraper object 

def main():
    Gameweeks = Scraper('get_bootstrap_static', 'events')
    data = Gameweeks.data 
    write_to_file(Gameweeks.data)

if __name__ == "__main__":
    main()

# NOTES:
# - Maybe I could think about placing some of this in the fpl_config file?
# - This might make sense because I have to make changes to the db init file as well
# - In that case maybe I could try to make that change after 


