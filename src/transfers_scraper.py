import requests
import json
import sys 
import codecs
import pprint 
import datetime

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# Let's think about the operations that I have to go through in order to accomplish the task of pulling the transfer data and costs of all the players


# Send a request to the bootstrap-static endpoint save as a json 
def get_bootstrap():
    request = requests.get(url)
    data = request.json()
    return data

# Pull elements from the bootstrap-static and save to its own json
def get_elements():
    elements = get_results()['elements']
    return elements

# Parses transfer and selection data
def filter_elements():

    current_time = datetime.datetime.now().isoformat()

    filtered_elements_json = {'filtered_elements' : []}

    for element in get_elements():
        filtered_elements_json['filtered_elements'].append({'id' : element['id'],
            'first_name': element['first_name'],
            'second_name': element['second_name'],
            'selected_by_percent': element['selected_by_percent'],
            'transfers_in': element['transfers_in'],
            'transfers_out': element['transfers_out'],
            'api_request_ts': current_time}) # No need to to run datetime.datetime.now() for ever loop, seems wasteful to do so
                             

    return filtered_elements_json

# Doing some thinking out loud here...
"""
I need to define and elements_filtered object
The key is going to be elements_filtered and it's going to store an array of dimensions 7 (includes the timestamp) x 516 to start
It'll look like this:
{
    "filtered_elements":[
        {"id": element['id'], "first_name": element['first_name'], etc...}
    ]
}

What happens is that I'm adding a new element to the filter_elements list inside the JSON object. 
For element in elements, add the filtered element to the list, each element is going to be a dictionary

I'll have to think about the method I need to call to update the filter_elements key...
"""


# Main function
def main():
    data = filter_elements()
    pp = pprint.PrettyPrinter()
    pp.pprint(data)
    export_file = open("../data/data_fpl_transfers.txt" , "w")
    json.dump(data, export_file)
    export_file.close()

if __name__ == "__main__":
    main()

# I want to reach the end goal of a json with all the players and their transfers in and out as well as they selected percent and cost...
# It needs to follow a JSON format
# What I have is not in JSON format...

#TODO modify the function so that it outputs a JSON which could be loaded into BigQuery~