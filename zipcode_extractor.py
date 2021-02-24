#!/usr/bin/env python3

import requests

res = requests.get("https://raw.githubusercontent.com/millbj92/US-Zip-Codes-JSON/master/USCities.json")

cities = res.json()
by_state = {}
for city in cities:
    print("%05d" % city["zip_code"])
    if city["state"] not in by_state:
        by_state[city["state"]] = ["%05d" % city["zip_code"]]
    else:
        by_state[city["state"]].append("%05d" % city["zip_code"])

for k,v in by_state.items():
    with open("zipcodes_by_states/%s.txt" % k, "w") as f:
        for zipcode in v:
            f.write(zipcode + "\n")
