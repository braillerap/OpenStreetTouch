import sys
import os
import json
import time

print ("Test OSM extract transport data")

def build_city_svg (city, transport, iso639_code = "fr"):
    osm = OSMprocess.Osmprocess()
    print ("running on ", city, transport)
    start = time.time ()
    osm.ReadTransportData(city, transport)
    end = time.time()
    osmdelay = end - start

    start = time.time ()
    transport_lines = osm.GetTransportDataLineList()
    end = time.time ()
    linelistdelay = end - start

    for line in transport_lines["lines"]:
        print (line)
    
    print ("timing")
    print ("osm delay", osmdelay)
    print ("linelist delay", linelistdelay)
    
    selected = []
    id = 0
    for line in transport_lines["lines"]:
        #print (line)
        selected.append({"id": id, "name": line, "select":True})
        id +=1
    
    # print (selected)
    
    graph_data = osm.GetTransportDataGraphInfo (selected)
    svg = osm.GetTransportDataSvg(selected, True, 2, False)
    with open("./examples/" + city + "_" + transport +'_station_test.svg', 'w') as f:
        f.write(str(svg))
    graph_data = osm.GetTransportDataGraphInfo (selected)
    svg = osm.GetTransportDataSvg(selected, True, 1, False)
    with open("./examples/" + city + "_" + transport +'_ways_test.svg', 'w') as f:
        f.write(str(svg))
    

if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    
    city = ""
    transport = ""
    from osm import OSMprocess
    
    test_data = [
        {"city": "amsterdam",   "transport": "subway"},
        {"city": "londres",     "transport": "subway"},
        {"city": "rennes",      "transport": "subway"},
        {"city": "lyon",        "transport": "subway"},
        {"city": "marseille",   "transport": "subway"},
        {"city": "paris",       "transport": "subway"},
        {"city": "berlin",      "transport": "subway"},
        {"city": "barcelone",    "transport": "subway"},
        {"city": "lyon",        "transport": "funicular"},
        {"city": "paris",       "transport": "funicular"},
        {"city": "paris",       "transport": "tram"},
        {"city": "nantes",       "transport": "tram"},
        {"city": "rennes",       "transport": "bus"},
        {"city": "prague",       "transport": "tram"},
        {"city": "milan",       "transport": "tram"},
        {"city": "los angeles",       "transport": "light_rail"},
        {"city": "bruxelles",       "transport": "tram"},
        {"city": "bruxelles",       "transport": "subway"},
    ]
    for data in test_data:
        build_city_svg (data["city"], data["transport"])
    