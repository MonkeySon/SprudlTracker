import json
import sys

import EControlParser
import IqCardParser
import InfluxDBConnector

CONFIG_FILE_NAME = 'config.json'

if len(sys.argv) == 2:
    CONFIG_FILE_NAME = sys.argv[1]
elif len(sys.argv) > 2:
    print(f'Usage: {sys.argv[0]} [ CONFIG_FILE ]')
    exit(1)

print(f'Using config file: {CONFIG_FILE_NAME}')

with open(CONFIG_FILE_NAME, encoding='UTF-8') as config_file:
    cfg = json.load(config_file)

eControlCfg = cfg['eControl']
iqCardCfg   = cfg['iqCard']
influxDBCfg = cfg['influxDB']

fuelPoints = []

if eControlCfg['enabled'] == True:
    fuelPoints += EControlParser.parse(eControlCfg)

if iqCardCfg['enabled'] == True:
    fuelPoints += IqCardParser.parse(iqCardCfg)

if influxDBCfg['enabled'] == True:
    if len(fuelPoints) > 0:
        InfluxDBConnector.write_points(influxDBCfg, fuelPoints)
    else:
        print('WARNING: No fuel points collected!')