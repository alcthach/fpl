import requests
import time
import json
import datetime
from scraper import Scraper

# TODO Adjust timestamp to have up to the minute?

def get_timestamp():
    timestamp = datetime.datetime.now().isoformat()     
    return timestamp  

def write_to_file(data):
    timestamp = get_timestamp()
    with open(f"../data/transfers/transfers_hourly_snapshot_{get_timestamp()}.txt", "w") as export_file:
        json.dump(data, export_file)

def get_transfers_snapshot(data):
    transfers_data = [ ] 
    for player in data:
       transfers_data.append(
                            {'id' : player['id'],
                             'transfers_in': player['transfers_in'],
                             'transfers_out': player['transfers_out'],
                             'timestamp': get_timestamp()})
    print("Successfully pulled transfers snapshot!)
    return transfers_data

def main():
    Players = Scraper('get_bootstrap_static', 'elements')
    data = Players.data    
    transfers_data = get_transfers_snapshot(data)
    write_to_file(transfers_data)

if __name__ == "__main__":
    main()
