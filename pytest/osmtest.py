import sys
import os
import json

print ("coucou")


if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    city = "rennes"
    transport = "subway"
    from osm import OSMprocess
    
    osm = OSMprocess.Osmprocess()
    print ("running on ", city, transport)
    osm.ReadTransportData(city, transport)
    

    ret = osm.GetTransportLineList()

    print ('#####################################')
    print ('########### line list ###############')
    print (ret)
    print (json.dumps(ret, indent=4, sort_keys=False))

    selected = []
    id = 0
    for line in ret["lines"]:
        print (id, line)
        selected.append({"id": id, "name": line, "select":True})
        id += 1
    print (selected)

    
    print ('#####################################')
    print ('########### build svg ###############')    
    svg = osm.get_svg (selected)
    print ('#####################################')
    print ('########### svg #####################')    
    #print (svg)

    

    