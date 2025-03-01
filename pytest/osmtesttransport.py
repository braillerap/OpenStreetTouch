import sys
import os
import json
import time

print ("Test OSM extract transport data")


if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    city = "Lyon"
    transport = "subway"
    from osm import OSMprocess
    
    osm = OSMprocess.Osmprocess()
    print ("running on ", city, transport)
    start = time.time ()
    nbresult = osm.ReadTransportData(city, transport)
    end = time.time()
    osmdelay = end - start
    print ("nbresult", nbresult)
    if nbresult > 0:
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
            print (line)
            selected.append({"id": id, "name": line, "select":True})
            id +=1
        selected[1]["select"] = True
        selected[-2]["select"] = True
        
        #print (selected)

        graph_data = osm.GetTransportDataGraphInfo (selected)
        
        #for line in graph_data:
            #print (line["name"])
            #print ('#' * 20)
            #for station in line["stations"]:
            #    print (line["name"],":",station)
            #print (line)
        
        print ("*" * 50)
        print ("*" * 10, "Build SVG")
        print ("*" * 50)
        svg = osm.GetTransportDataSvg(selected, True, False)
        
        with open ("test.svg", "w") as f:
            f.write (svg)
   