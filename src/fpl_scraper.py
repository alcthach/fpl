from random import expovariate
import requests
import time
import json
import sys
import codecs
import csv


class FplScraper:

    api_call_type = ""
    config_file = "fpl_config.json"

    def get_results(self, config_data):
        request = requests.get(config_data[self.api_call_type]['api_endpoint'])
        data = request.json()
        return data

    def main(self, p_config_file):
        response = self.get_results(p_config_file)
        data = response
        export_file = open("../data/data_" + self.api_call_type + ".txt" , "w")
        json.dump(data, export_file)
        export_file.close()

    def __init__(self, api_call_type):
        self.api_call_type = api_call_type
        config = open(self.config_file)
        config_data = json.load(config)
        self.main(config_data)

# FplScraper('get_bootstrap_static') For testing purposes


"""
Pseudocode

def __init__(self, api_call_type):
    FplScraper object now has an attribute called api_call_type; when I instantiate the object I will pass the type of call I want to make
    instantiate an object called config, we open the json file, I'm not sure why self. is included in the pattern...
    takes the file object and returns the json object, reads json encoded data and converts to python dict, saved to object
    self.main(config_data) this one is a bit strange to me... it seems like when someone instantiates the FplScraper object that it will just run main
    I don't think I have to have that line of code there if I don't need it
    
"""