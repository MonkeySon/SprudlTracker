import json
import sys
import traceback

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

try:
    with open(CONFIG_FILE_NAME, encoding='UTF-8') as config_file:
        cfg = json.load(config_file)
except Exception as e:
    print('Exception while opening config file:', e)
    print(traceback.format_exc())

eControlCfg = cfg['eControl']
iqCardCfg   = cfg['iqCard']
influxDBCfg = cfg['influxDB']

fuelPoints = []

try:
    if eControlCfg['enabled'] == True:
        fuelPoints += EControlParser.parse(eControlCfg)
except Exception as e:
    print('Exception while parsing E-Control:', e)
    print(traceback.format_exc())

try:
    if iqCardCfg['enabled'] == True:
        fuelPoints += IqCardParser.parse(iqCardCfg)
except Exception as e:
    print('Exception while parsing IQ Card:', e)
    print(traceback.format_exc())

try:
    if influxDBCfg['enabled'] == True:
        if len(fuelPoints) > 0:
            InfluxDBConnector.write_points(influxDBCfg, fuelPoints)
        else:
            print('WARNING: No fuel points collected!')
except Exception as e:
    print('Exception while writing points to InfluxDB:', e)
    print(traceback.format_exc())