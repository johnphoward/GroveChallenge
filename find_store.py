from csv import DictReader
from json import dumps
from argparse import ArgumentParser
from math import radians, sin, cos, sqrt, asin
from queue import PriorityQueue
from geopy.geocoders import Nominatim


TEXT = 'text'
JSON = 'json'
MILES = 'mi'
KILOMETERS = 'km'
MILES_PER_KM = 0.621371
EARTH_KM_RADIUS = 6372.8


class LocationFinder:

    def __init__(self):
        self.store_csv = 'store-locations.csv'

        self.store_list = []

        with open(self.store_csv) as f:
            reader = DictReader(f)
            for row in reader:
                store_location = '{address}, {city}, {state} {zip}'.format(address=row['Address'], city=row['City'],
                                                                           state=row['State'], zip=row['Zip Code'])
                store_latitude = float(row['Latitude'])
                store_longitude = float(row['Longitude'])

                self.store_list.append((store_location, store_latitude, store_longitude))

    @staticmethod
    def find_location_latlon(given_location):
        geocoder = Nominatim()
        location = geocoder.geocode(given_location)

        return location.latitude, location.longitude

    @staticmethod
    def haversine_distance(lat_1, lon_1, lat_2, lon_2):

        d_lat = radians(lat_2 - lat_1)
        d_lon = radians(lon_2 - lon_1)
        lat1 = radians(lat_1)
        lat2 = radians(lat_2)

        a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
        c = 2 * asin(sqrt(a))

        return EARTH_KM_RADIUS * c

    def find_nearest_location_and_distance(self, query):
        distance_queue = PriorityQueue()

        current_latitude, current_longitude = self.find_location_latlon(query)

        for store_name, store_latitude, store_longitude in self.store_list:
            distance = self.haversine_distance(current_latitude, current_longitude, store_latitude, store_longitude)
            distance_queue.put((distance, store_name))

        return distance_queue.get()

    @staticmethod
    def output_information(store_text, distance, units, output_type=TEXT):
        distance = round(distance, 3)
        if output_type == TEXT:
            print('Nearest store address: {address}'.format(address=store_text))
            print('Distance: {distance} {units}.'.format(distance=distance, units=units))
        else:
            print(dumps({
                'distance': distance,
                'address': store_text,
                'units': units
            }))

    def handle_request(self, location=None, units=MILES, output=TEXT):
        distance, store_text = self.find_nearest_location_and_distance(location)

        final_distance = distance * MILES_PER_KM if units == MILES else distance

        self.output_information(store_text, final_distance, units, output)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--address', action='store', dest='location')
    parser.add_argument('--zip', action='store', dest='location')
    parser.add_argument('--units', action='store', choices=[KILOMETERS, MILES], dest='units', default=MILES)
    parser.add_argument('--output', action='store', choices=[TEXT, JSON], dest='output', default=TEXT)

    args = vars(parser.parse_args())
    location_finder = LocationFinder()
    location_finder.handle_request(location=args['location'], units=args['units'], output=args['output'])
