from . import application_OSM_extraction 
from . import OSMsvg
from . import OSMGeometry
from . import OSMTransitInfo
from . import OSMsvgFile
from . import OSMStreetMap

import pandas as pd
import json

class Osmprocess:
    def __init__(self):
        self.osm_data = None
        self.CityName = ""
        self.transport_type = "subway"
        self.iso639_code = "fr"
        self.transit_info = OSMTransitInfo.OSMTransitInfo()

        self.streetmap_data = None

    def ReadTransportData (self, city, transport_type, iso639_code = "fr"):
        self.CityName = city.title()
        self.transport_type = transport_type
        self.iso639_code = iso639_code
        
        # extract osm data with overpass request
        self.osm_data = application_OSM_extraction.overpass_request(self.CityName, transport_type, iso639_code)
        #json.dump (self.osm_data, open("osm_request.json", "w"), indent=4, sort_keys=False)
        
        # data structuration for future usage
        self.transport_data = application_OSM_extraction.osm_extraction (self.osm_data, self.CityName, self.transport_type)
        #json.dump (self.transport_data, open("osm_extraction.json", "w"), indent=4, sort_keys=False)
        
        return len(self.transport_data["relations"])
        
    def GetTransportDataLineList (self):
        
        # extract transport lines from relations
        transport_lines = application_OSM_extraction.osm_get_transport_lines (self.transport_data, self.transport_type)
        
        # sort data
        transport_lines.sort(key=lambda x: x["name"])
        result = {"city":self.CityName, "lines":[line["name"] for line in transport_lines]} 
        return result
    

    def GetTransportDataGraphInfo (self, linelist):
        desired_line = [line["name"] for line in linelist if line["select"] == True]
        
        transport_graph_data = application_OSM_extraction.osm_extract_data (self.transport_data, self.transport_type)
        
        transit = application_OSM_extraction.osm_build_transit_table(transport_graph_data)
        self.transit_info.SetStationInfos (transit)

        transport_graph_data_filtered = application_OSM_extraction.osm_filter_transport_lines_data (transport_graph_data, desired_line)
        
        json.dump (transit, open("transit_data.json", "w"), indent=4, sort_keys=False)
        json.dump (transport_graph_data_filtered, open("transport_graph_data.json", "w"), indent=4, sort_keys=False)
        return transport_graph_data_filtered
    
    def GetTransportDataSvg (self, linelist, drawstations, linestrategy):
        graph_data = self.GetTransportDataGraphInfo (linelist)
        width = 1500
        height = 1000
        marginx = 50
        marginy = 50
        
        fsvg = OSMsvgFile.OSMsvgFile ()
        fsvg.open (widthmm=width, heightmm=height)
        
        engine = OSMGeometry.OsmTransportDrawing ()
        engine.build_projected_data (graph_data, width=width, height=height, marginx=marginx, marginy=marginy)
        
        if linestrategy == 0:
            engine.fill_hole = False  
            engine.build_poly_from_ways (fsvg, width, height, marginx, marginy)
        elif linestrategy == 1:  
            engine.fill_hole = True  
            engine.build_poly_from_ways (fsvg, width, height, marginx, marginy)
        elif linestrategy == 2:
            engine.build_poly_from_stations (fsvg, width, height, marginx, marginy)
        
        if drawstations:
            engine.build_stations (fsvg, width, height, marginx, marginy)

        fsvg.close ()
        
        return str(fsvg.getSVGString())

    def GetTransportLineList (self):
        if (len(self.osm_data) == 0):
            return None
        ret = application_OSM_extraction.line_extraction_and_stations (self.osm_data)
        #ret = application_OSM_extraction.line_extraction (self.osm_data)
        
        print ("line_extraction_and_stations")
        print (json.dumps(ret, indent=4, ensure_ascii=False))
        #print (type(ret))
        
        list = []
        for line in ret:
            #print (line["line_label"], line["line_name"])
            if (line["line_name"] not in list):
                list.append (line["line_name"])
        result = {"city":self.CityName, "lines":list}    
        return result
    
    
    

    
    

if __name__ == "__main__":
    osm = Osmprocess()
    osm.ReadTransportData("rennes", "subway")
    ret = osm.GetLineList()
    print ('########### final ###############')
    print (ret)

    osm.get_svg()