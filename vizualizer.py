import folium
import json


class Vizualizer:
    def __init__(self, lat, long, datafile) -> None:
        self.lat = lat
        self.long = long
        self.datafile = datafile

    def save_map(self):
        mapt = folium.Map(location=[self.lat, self.long],
                          zoom_start=10, tiles="OpenStreetMap")

        with open(self.datafile, 'r') as f:
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
