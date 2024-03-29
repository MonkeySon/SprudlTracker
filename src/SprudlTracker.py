import json
import sys
import traceback

import MailifierUtil
import EControlParser
import IqCardParser
import InfluxDBConnector

MAILIFIER_ENABLE = True
MAILIFIER_TAG = 'SprudlTracker'

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
    if MAILIFIER_ENABLE:
        MailifierUtil.mailify_exception(MAILIFIER_TAG, 'Exception while opening config')

eControlCfg = cfg['eControl']
iqCardCfg   = cfg['iqCard']
influxDBCfg = cfg['influxDB']

fuelPoints = []

try:
    if eControlCfg['enabled'] == True:
        print("Parsing E-Control ...")
        fuelPoints += EControlParser.parse(eControlCfg)
    else:
        print("Skipping E-Control ...")
except Exception as e:
    print('Exception while parsing E-Control:', e)
    print(traceback.format_exc())
    if MAILIFIER_ENABLE:
        MailifierUtil.mailify_exception(MAILIFIER_TAG, 'Exception E-Control parsing')

try:
    if iqCardCfg['enabled'] == True:
        print("Parsing IQ Card ...")
        fuelPoints += IqCardParser.parse(iqCardCfg)
    else:
        print("Skipping IQ Card ...")
except Exception as e:
    print('Exception while parsing IQ Card:', e)
    print(traceback.format_exc())
    if MAILIFIER_ENABLE:
        MailifierUtil.mailify_exception(MAILIFIER_TAG, 'Exception IQ Card parsing')

try:
    if influxDBCfg['enabled'] == True:
        print("Writing to InfluxDB ...")
        if len(fuelPoints) > 0:
            InfluxDBConnector.write_points(influxDBCfg, fuelPoints)
        else:
            print('WARNING: No fuel points collected!')
    else:
        print("Skipping InfluxDB ...")
except Exception as e:
    print('Exception while writing points to InfluxDB:', e)
    print(traceback.format_exc())
    if MAILIFIER_ENABLE:
        MailifierUtil.mailify_exception(MAILIFIER_TAG, 'Exception InfluxDB writing')
