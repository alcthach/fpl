'''
FPL API Scraper
Alex Thach - alcthach@gmail.com
2022-07-06
'''

import pprint
import requests
import time
import json
import sys
import codecs
import csv
import datetime

"""

TODO: 

- Refactor code to include:
    - Transfers snapshot
    - Player snapshot
    - Time stamp for when pull was completed

- Let's see if I can understand the code below first...

"""


class Scraper:

    api_call_type = ""
    config_file = "fpl_config.json"

    def get_results(self, config_data):
        request = requests.get(config_data[self.api_call_type]['api_endpoint'])
        self.data = request.json()[self.key]
        return self.data

    def get_player_value_snapshot(self, data):
        pass

    def get_transfers_snapshot(self, data):

        current_time = datetime.datetime.now().isoformat()

        transfers_data = [] #{'filtered_elements' : []}

        for element in data:
           transfers_data.append({'id' : element['id'],
                                  'transfers_in': element['transfers_in'],
                                  'transfers_out': element['transfers_out'],
                                  'timestamp': current_time}) 

        return transfers_data

    # Trying out the with open() pattern, handles exceptions better and is a better cleaner
    # TODO: add {datetime.datetime.now().isoformat()} to filename? have to adjust the load scripts
    # Re: Check for the newest file to load, then check the rows, change data capture...
    def write_to_file(self, data):
        # export_file = open(f"../data/{self.api_call_type}_{self.key}.txt", "w") 
        with open(f"../data/{self.api_call_type}_{self.key}.txt", "w") as export_file:
            json.dump(data, export_file)
        # export_file.close()

    def main(self, p_config_file): # Q: Why is config_file prefixed with "_p"?
        data = self.get_results(p_config_file) # Why p_config_file and not config_data?
        transfers_data = self.get_transfers_snapshot(data)
        print(transfers_data)
        # write_to_file(data)

    def __init__(self, api_call_type, key = None):
        self.api_call_type = api_call_type
        self.key = key
        config = open(self.config_file)
        config_data = json.load(config)
        self.main(config_data) # main() is called when the class is initialized? Yes

keys_lst = ['events', 'game_settings', 'phases', 'teams', 'total_players', 'elements', 'element_stats', 'element_types']

# for key in keys_lst:
    # Scraper('get_bootstrap_static', key)

# Hard-coded here. I might need a separate scripts or modules to pull differen snapshots
# Or update tables in the case of 'events'
# And I also have a initial load with the dimensions tables to some extent like teams? or phases 
# Or element-types
# Still outstanding is some dimensional modelling
# For now I'm taking care of the staging layer tables!
Scraper('get_bootstrap_static', 'elements' ) # Hardcoded to pull from elements to make possible to get transfer data, TODO: refactor into it's own module perhaps... or at least clean this up
