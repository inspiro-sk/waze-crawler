import json
import os
from datetime import datetime


def read_logfile(logfile):
    with open(logfile, 'r') as f:
        data = f.readlines()

        for row in data:
            items = row.rstrip().split('\t')
            timestamp = items[0]
            coords = json.loads(items[1])

            for coord in coords:
                print(
                    f"lat: {coord['lat']}, lon: {coord['long']}, type: {coord['type']}")


read_logfile('police_coordinates.log')
