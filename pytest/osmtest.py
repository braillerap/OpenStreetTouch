import sys
import os


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
    osm.ReadTransportData("rennes", "subway")
    
    ret = osm.GetTransportLineList()

    print ('#####################################')
    print ('########### line list ###############')
    print (ret)

    svg = osm.get_svg ()
    print ('#####################################')
    print ('########### svg #####################')    
    #print (svg)

    

    