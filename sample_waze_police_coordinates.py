#!/usr/bin/env python3

import json
import datetime
import requests


def get_waze_reports():
    headers = {
        "referer": "https://www.waze.com/live-map",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    r = requests.get(
        "https://www.waze.com/row-rtserver/web/TGeoRSS?bottom=48.10745091736649&left=17.101683197021488&ma=200&mj=200&mu=20&right=17.504045867919925&top=48.34650365458537", headers=headers)
    r.raise_for_status()
    alerts = r.json().get('alerts', [])
    alerts = filter(lambda x: x['type'] in ['POLICE', 'ACCIDENT'], alerts)
    locations = map(lambda x: dict(
        type=x['type'], lat=x['location']['y'], long=x['location']['x']), alerts)
    locations = list(locations)
    return locations


content = json.dumps(get_waze_reports())
timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)

with open("police_coordinates.log", "a") as f:
    f.write('{}\t{}\n'.format(timestamp, content))
