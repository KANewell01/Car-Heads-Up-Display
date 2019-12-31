# OSRM interface object
# Gives a set of easy to use functions for finding routes
# 
# 11/29/19
# Kevin Newell

import requests
import json
from urllib.parse import quote

# Manuever datatype
class maneuver:
    bearing_before = None
    bearing_after = None
    mtype = None
    modifier = None
    location = None
    # def __init__(self, bearing_before, bearing_after, mtype, modifier, location):
    #     self.bearing_before = bearing_before
    #     self.bearing_after = bearing_after
    #     self.mtype = mtype
    #     self.modifier = modifier
    #     self.location = location


# OSRM interface
class osrm:
    # Interface must be initialized with a domain hosting the service, local or otherwise
    def __init__(self, domain):
        self.domain = domain

    # Returns a tuple with route based on a given set of coordinates, a source and a destination
    # and an estimated ETA, in seconds(float), to the destination
    def route(self, src, dst):
        nav = 'route/v1/driving/' + src + ';' + dst + '?overview=false&steps=true'
        reply = requests.get(self.domain + nav)
        data = json.loads(reply.text)

        maneuvers = []
        eta = 0.0
        for i in range(len(data["routes"][0]["legs"][0]["steps"])):
            maneuvers.append(maneuver())
            maneuvers[-1].bearing_before = data["routes"][0]["legs"][0]["steps"][i]["maneuver"]["bearing_before"]
            maneuvers[-1].bearing_after = data["routes"][0]["legs"][0]["steps"][i]["maneuver"]["bearing_after"]
            maneuvers[-1].mtype = data["routes"][0]["legs"][0]["steps"][i]["maneuver"]["type"]
            maneuvers[-1].location = data["routes"][0]["legs"][0]["steps"][i]["maneuver"]["location"]
            if "modifier" in data["routes"][0]["legs"][0]["steps"][i]["maneuver"]:
                maneuvers[-1].modifier = data["routes"][0]["legs"][0]["steps"][i]["maneuver"]["modifier"]

            eta += data["routes"][0]["legs"][0]["steps"][i]["duration"]

        return (maneuvers, eta)

    # Convert an address into a set of coordinates to find
    ## Returns a string in the form "<lon,lat>"
    def geocode(self, addr):
        MAPQUEST = "http://open.mapquestapi.com/nominatim/v1/search.php?key=mh1dCUI5eg6G0BGX7NZMhJGkRhvGjTnd&format=json&q="
        query = quote(addr)

        response = requests.get(MAPQUEST + query)
        data = json.loads(response.text)
        geocode = data[0]["lon"] + ',' + data[0]["lat"]
        
        return geocode
