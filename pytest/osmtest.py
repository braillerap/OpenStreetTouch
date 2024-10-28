import sys
import os





if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from osm import OSMprocess
    
    osm = OSMprocess.Osmprocess()
    osm.ReadTransportData("rennes", "subway")
    ret = osm.GetTransportLineList()
    print ('#####################################')
    print ('########### line list ###############')
    print (ret)

    svg = osm.get_svg ()
    print ('#####################################')
    print ('########### svg #####################')    
    #print (svg)

    

    