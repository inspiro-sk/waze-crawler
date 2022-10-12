import requests


class Crawler:
    def __init__(self, lat, long, types=None) -> None:
        self.headers = {
            "referer": "https://www.waze.com/live-map",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

        self.lat = lat
        self.long = long
        self.types = types if types is not None else ["POLICE", "ACCIDENT"]

        self.georss_params = {
            "bottom": self.lat,
            "left": self.long,
            "ma": 200,  # alerts
            "mj": 200,  # users
            "mu": 20,  # jams
            "right": self.long + 0.4,
            # TODO can be parameterized later (consume input from fronend)
            "top": self.lat + 0.4,
        }

    def get_georss_params(self):
        return self.georss_params

    def get_tgeorss_uri(self):
        tgeorss_uri = f"https://www.waze.com/row-rtserver/web/TGeoRSS?bottom=\
            {self.georss_params['bottom']}&left={self.georss_params['left']}&ma={self.georss_params['ma']}&mj={self.georss_params['mj']}&mu={self.georss_params['mu']}&right={self.georss_params['right']}&top={self.georss_params['top']}"

        return tgeorss_uri

    def get_reports(self):
        tgeorss_uri = self.get_tgeorss_uri()

        r = requests.get(tgeorss_uri, headers=self.headers)
        r.raise_for_status()

        alerts = r.json().get('alerts', [])
        alerts = filter(lambda x: x['type'] in ['POLICE', 'ACCIDENT'], alerts)

        locations = map(lambda x: dict(
            type=x['type'], lat=x['location']['y'], long=x['location']['x']), alerts)
        locations = list(locations)

        return locations
