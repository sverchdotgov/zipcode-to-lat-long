#!/user/bin/env python3

import requests
import os
import sys
import time
import json

mapbox_access_token = os.environ.get("MAPBOX_ACCESS_TOKEN")
if not mapbox_access_token:
    print("Must set MAPBOX_ACCESS_TOKEN!")
    sys.exit(1)
session = requests.Session()

def build_mapbox_url(zipcode, access_token):
    return "https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json?country=us&types=postcode&autocomplete=false&access_token=%s" % (zipcode, access_token)

def create_zipcode_to_latlon(zipcode):
    zipcode_to_lat_lon = {}
    with open(sys.argv[1]) as f:
        num_searched = 0
        for zipcode in f:
            mapbox_url = build_mapbox_url(zipcode, mapbox_access_token)
            mapbox_res = session.get(mapbox_url)
            if len(mapbox_res.json()["features"]) < 1:
                print("Mapbox result doesn't have features for zipcode %s" % zipcode)
                continue
            (lon, lat) = mapbox_res.json()["features"][0]["center"]
            zipcode_to_lat_lon[zipcode.rstrip()] = [lat, lon]
            if num_searched % 100 == 0:
                print("Searched for %s zipcodes." % num_searched)
            num_searched += 1
        return zipcode_to_lat_lon

def main():
    if len(sys.argv) != 3:
        print("Usage: %s <one_per_line_zipcode_file> <destination>" % sys.argv[0])
        sys.exit(1)
    with open(sys.argv[2], "w") as f:
        f.write(json.dumps(create_zipcode_to_latlon(sys.argv[1])))
main()
