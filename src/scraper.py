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

        filtered_elements = {'filtered_elements' : []}

        for element in data:
            filtered_elements['filtered_elements'].append({'id' : element['id'],
                                                           'transfers_in': element['transfers_in'],
                                                           'transfers_out': element['transfers_out'],
                                                           'timestamp': current_time}) # No need to to run datetime.datetime.now() for ever loop, seems wasteful to do so

        return filtered_elements


    def main(self, p_config_file): # Q: Why is config_file prefixed with "_p"?
        data = self.get_results(p_config_file) # Why p_config_file and not config_data?
        # data = self.filter_results(data)
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        pp.pprint(data)
        # export_file = open(f"../data/data_fpl_transfers_{datetime.datetime.now().isoformat()}.txt" , "w")
        export_file = open(f"../data/{self.api_call_type}_{self.key}.txt", "w") 
        json.dump(data, export_file)
        export_file.close()

        # I need to pull my elements from the json object... found in transfers_scraper.py

    def __init__(self, api_call_type, key = None):
        self.api_call_type = api_call_type
        self.key = key
        config = open(self.config_file)
        config_data = json.load(config)
        self.main(config_data) # main() is called when the class is initialized? Yes

# Let's just go with hard-coded method for now, I'll make revisions later on
# Just want to get it working for now!
# TODO Make sure to have timestamp columns for all the tables!
# Going to need a different script for batch loads, this one can be an initial load
keys_lst = ['events', 'game_settings', 'phases', 'teams', 'total_players', 'elements', 'element_stats', 'element_types']

for key in keys_lst:
    Scraper('get_bootstrap_static', key)

