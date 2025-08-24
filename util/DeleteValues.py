import sys
import traceback
import json

from influxdb_client import InfluxDBClient

CONFIG_FILE_NAME = 'config.json'

def delete_points(config):
    client = InfluxDBClient(url=config['url'], token=config['token'], org=config['org'])
    delete_api = client.delete_api()
    start = "1970-01-01T00:00:00Z"
    stop = "2024-01-04T00:00:00Z"
    delete_api.delete(start, stop, f'_measurement="{config["measurement"]}"', bucket=config['bucket'], org=config['org'])
    client.close()

if __name__ == '__main__':
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

    influxDBCfg = cfg['influxDB']

    delete_points(influxDBCfg)