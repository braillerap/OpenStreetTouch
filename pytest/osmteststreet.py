import sys
import os
import time

london = [51.51340370316125, -0.08893059482409707]

if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    
    from osm import OSMprocessStreet
    
    osm = OSMprocessStreet.OSMprocessStreet()
    print ("running on ", london)
    start = time.time ()
    map = osm.ReadStreetMapData(london[0], london[1], 80) 
    end = time.time()
    osmdelay = end - start
    
    
        
    print ("timing")
    print ("osm delay", osmdelay)
    
    
    
    svg = osm.GetStreetMapSVG(map)
    
    with open ("street.svg", "w") as f:
        f.write (svg)
