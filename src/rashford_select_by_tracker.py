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
                          'selected_by_pct' : rashford_data['selected_by_percent'],
                          'timestamp': current_time
        }

with open(f"/home/alext/work/projects/fpl/data/test/rashford_selected_by_log.txt", "a" ) as export_file:
    json.dump(rashford_transfers_data, export_file)

    
