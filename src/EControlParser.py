import requests
from FuelPoint import FuelPoint

def parse(config):
    points = []
    for fuelType in config['fuelTypes']:
        for location in config['locations']:
            payload = {
                'fuelType': fuelType,
                'includeClosed': config['includeClosed'],
                'latitude': location['lat'],
                'longitude': location['lon']
            }
            resp = requests.get(config['endpoint'], params=payload)
            resp_json = resp.json()
            for resp_entry in resp_json:
                if resp_entry['position'] == 1:
                    price = resp_entry['prices'][0]['amount']

                    fullfuelType = 'Unknown'
                    if fuelType == 'DIE':
                        fullfuelType = 'Diesel'
                    elif fuelType == 'SUP':
                        fullfuelType = 'Super'

                    points += [FuelPoint(location['name'], fullfuelType, price)]
                    break
    return points