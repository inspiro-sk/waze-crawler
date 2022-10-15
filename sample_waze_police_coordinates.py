#!/usr/bin/env python3

import json
import datetime
from crawler import Crawler
from vizualizer import Vizualizer


def get_waze_reports(lat, long):
    c = Crawler(lat, long, ["POLICE", "ACCIDENT"])
    return c.get_reports()


if __name__ == "__main__":
    lat = 49.01479241812091
    long = 19.36074256896973

    content = get_waze_reports(lat, long)
    timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)

    with open("police_coordinates.log", "a") as f:
        f.write('{}\t{}\n'.format(timestamp, content))

    v = Vizualizer(lat, long, f.name)
    v.save_map()
