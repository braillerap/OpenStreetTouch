from . import application_OSM_extraction 
from . import OSMsvg
import pandas as pd
import json

class Osmprocess:
    def __init__(self):
        self.osm_data = None
        self.CityName = ""
        self.transport_type = "subway"
        self.iso639_code = "fr"

    def ReadTransportData (self, city, transport_type, iso639_code = "fr"):
        self.CityName = city.title()
        self.transport_type = transport_type
        self.iso639_code = iso639_code
        
        # extract osm data with overpass request
        self.osm_data = application_OSM_extraction.overpass_request(self.CityName, transport_type, iso639_code)
        json.dump (self.osm_data, open("osm_request.json", "w"), indent=4, sort_keys=False)
        
        # data structuration for future usage
        self.transport_data = application_OSM_extraction.osm_extraction (self.osm_data, self.CityName, self.transport_type)
        json.dump (self.transport_data, open("osm_extraction.json", "w"), indent=4, sort_keys=False)
        
        return len(self.transport_data)
        
    def GetTransportDataLineList (self):
        
        # extract transport lines from relations
        transport_lines = application_OSM_extraction.osm_get_transport_lines (self.transport_data, self.transport_type)
        
        # sort data
        transport_lines.sort(key=lambda x: x["name"])
        return transport_lines
    

    def GetTransportDataGraphInfo (self, linelist):
        desired_line = [line["name"] for line in linelist if line["select"] == True]
        transport_graph_data = application_OSM_extraction.osm_get_transport_lines_data (self.transport_data, desired_line, self.transport_type)
        
        return transport_graph_data
    
    def GetTransportDataSvg (self, graphdata):
        pass


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
    
    
    def get_svg (self, linelist):
        svg="<svg></svg>"
        if len (self.osm_data) == 0:
            return None
        print ("get_svg", linelist) 
        
        # build selected lines list
        desired_lines = [trline["name"] for trline in linelist if trline["select"] == True]

        print ("desired lines :" , desired_lines)                
        #data = application_OSM_extraction.plot_get_2d_data (self.osm_data, linelist)
        data = application_OSM_extraction.lines_ways_extraction_from_datta (self.osm_data)
        
        #data = self.line_extraction (self.osm_data)
        data.to_csv("line_extraction.csv", sep=';', index=False)
        # naive filtering panda dataframe
        #df = data.copy ()
        #df = df[df["line_name"].isin(desired_lines)]
        
        print ("#" * 25)
        print(data)
        print (type(data))
        #svg = OSMsvg.transport_data_to_svg (data)

        return str(svg)


    

if __name__ == "__main__":
    osm = Osmprocess()
    osm.ReadTransportData("rennes", "subway")
    ret = osm.GetLineList()
    print ('########### final ###############')
    print (ret)

    osm.get_svg()