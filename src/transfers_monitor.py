import requests 
import json
from datetime import datetime


now = datetime.now()

current_time = now.strftime("%H:%M:%S")

# Using this script to monitor changes in transfers

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

response = requests.get(url).json()

elements = response['elements']

# Monitors Marcus Rashford transfers

rashford_data = elements[392]

rashford_transfers_data = {
                          'transfers_in': rashford_data['transfers_in'],
                          'transfers_out': rashford_data['transfers_out'],
                          'net_transfers:': rashford_data['transfers_in'] - rashford_data['transfers_out'],
                          'timestamp': current_time
        }

with open(f"/home/alext/work/projects/fpl/data/transfers/monitoring/rashford_transfers_log.txt", "a" ) as export_file:
    json.dump(rashford_transfers_data, export_file)

    
