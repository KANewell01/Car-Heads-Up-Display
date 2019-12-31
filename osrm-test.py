import requests
import json

print("----OSRM API Test----\n")

DOMAIN = 'http://localhost:5000/'
# Home
SRC = '-94.366550,38.980449'
# School
DST = '-91.774779,37.951169'

# Build Request Endpoint
nav = 'route/v1/driving/' + SRC + ';' + DST + '?overview=false&steps=true'

# Send request to router
r = requests.get(DOMAIN+nav)

# Parse return data as json
data = json.loads(r.text)

# Iterate through 1st given route for maneuvers
eta = 0.0
for i in range(len(data["routes"][0]["legs"][0]["steps"])):
    print(data["routes"][0]["legs"][0]["steps"][i]["maneuver"])
    eta += data["routes"][0]["legs"][0]["steps"][i]["duration"]

print("\nETA: " + str(eta) + " seconds")

print("\n\n")
print("----OSRM Interface Class Test----\n")

from osrm import osrm

routing = osrm(DOMAIN)

route = routing.route(SRC, DST)
for i in range(len(route[0])):
    print(route[0][i].location, end=' ')
    print(route[0][i].modifier)

print("ETA: " + str(route[1]))

print("\n\n")
print("----Geocoding Test----\n")

route = routing.route(routing.geocode("kansas city"), routing.geocode("missouri s&t"))
for i in range(len(route[0])):
    print(route[0][i].location, end=' ')
    print(route[0][i].modifier)

print("ETA: " + str(route[1]))