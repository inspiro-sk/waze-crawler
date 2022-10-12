import json
import os
from datetime import datetime
from time import time
import psycopg2
import folium


def read_logfile(logfile):
    mapt = folium.Map(location=["48.17", "17.40"],
                      zoom_start=10, tiles="OpenStreetMap")

    with open(logfile, 'r') as f:
        data = f.readlines()

        for row in data:
            items = row.rstrip().split('\t')
            timestamp = items[0]
            coords = json.loads(items[1])

            for coord in coords:
                # print(timestamp, coord['lat'], coord['long'], coord['type'])
                if coord['type'] == 'POLICE':
                    folium.CircleMarker(
                        [coord['lat'], coord['long']],
                        fill=True,
                        color="blue",
                        fill_color="blue",
                        fill_opacity=1,
                        radius=2,
                    ).add_to(mapt)
                else:
                    folium.CircleMarker(
                        [coord['lat'], coord['long']],
                        fill=True,
                        color="red",
                        fill_color="red",
                        fill_opacity=1,
                        radius=2,
                    ).add_to(mapt)

    mapt.save("map.html")

    connect_db()


def connect_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(
            host="localhost",
            database="waze",
            user="rstana",
            password="wity457&T(#&RJYOSdt4ojf8wty07o45ghrfojd78g648zusdoihf"
        )

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        sql = """INSERT INTO coords(timestamp, lat, long, type)
             VALUES(%s, %s, %s, %s)"""
        cur.executemany(
            sql, [['1665124200895', '48.164593', '17.179617', 'ACCIDENT'], ['1665124200895', '48.164593', '17.179617', 'POLICE']])

        # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


read_logfile('police_coordinates.log')
