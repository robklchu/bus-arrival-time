#!/usr/bin/env python3
#
# bus-arrival.py
# ==============
# (written by Rob Chu)
# This program makes use of the Transport for London (TfL) Unified API to check the expected arrival times (in mins) of a bus route at a given bus stop 
# in London.
#
# Usage: ./bus-arrival.py bus_stop bus_route
# (Example: ./bus-arrival.py "Euston Square Station" 30)

import sys
import urllib.request
import json

if len(sys.argv) != 3:
    raise SystemExit("Usage: ./bus-arrival.py bus_stop bus_route")
else:
    stop = sys.argv[1]
    route = sys.argv[2]

# Find the National Public Transport Access Nodes (NaPTAN) id of a bus stop
def naptan(stop):
    naptanid = None
    stop_revised = stop.replace(" ", "%20")
    response = urllib.request.urlopen(f"https://api.tfl.gov.uk/StopPoint/Search/{stop_revised}")
    str_data = response.read().decode("utf-8")
    json_data = json.loads(str_data)
    if json_data["total"] == 1:
        naptanid = json_data["matches"][0]["id"]
    return naptanid

# Find the arrival time(s)
def arrival_times(naptanid, route):
    time_to_stop = []
    arr_response = urllib.request.urlopen(f"https://api.tfl.gov.uk/StopPoint/{naptanid}/arrivals")
    str_arrivals = arr_response.read().decode("utf-8")
    json_arrivals = json.loads(str_arrivals)
    buses = [bus for bus in json_arrivals if bus["lineName"] == route]
    if len(buses) > 0:
        time_to_stop = sorted([round(bus["timeToStation"] / 60) for bus in buses])
    return time_to_stop

def output(diff):
    if len(diff) == 0:
        print("NO INFO")
    else:    
        for d in diff:
            if d == 0:
                print("APPROACHING")
            elif d == 1:
                print(f"{d} MIN")
            else:
                print(f"{d} MINS")

# Main
id = naptan(stop)
if id is None:
    raise SystemExit(f"Invalid bus stop name and/or bus route: {stop}!")

diff = arrival_times(id, route)
print(f"The next Route {route} buses will arrive in:")
output(diff)
