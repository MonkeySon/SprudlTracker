from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from FuelPoint import FuelPoint

def write_points(config, fuelPoints):
    points = []

    fuelPoint: FuelPoint
    for fuelPoint in fuelPoints:
        points += [Point(config['measurement']).tag('location', fuelPoint.location).tag('fuelType', fuelPoint.fuelType).field('price', fuelPoint.price)]

    client = InfluxDBClient(url=config['url'], token=config['token'], org=config['org'])
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=config['bucket'], record=points)