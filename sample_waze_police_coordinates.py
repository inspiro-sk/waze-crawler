#!/usr/bin/env python3

import json
import datetime
from crawler import Crawler


def get_waze_reports():
    c = Crawler(49.01479241812091, 19.36074256896973, ["POLICE", "ACCIDENT"])
    locations = c.get_reports()

    return locations


content = json.dumps(get_waze_reports())
timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)

with open("police_coordinates.log", "a") as f:
    f.write('{}\t{}\n'.format(timestamp, content))
