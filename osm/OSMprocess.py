from . import application_OSM_extraction 
from . import OSMsvg

class Osmprocess:
    def __init__(self):
        self.osm_data = None
        self.CityName = ""

    def ReadTransportData (self, city, transport_type, iso639_code = "fr"):
        # todo : check capitals in name
        self.CityName = city.title()
        #self.osm_data = application_OSM_extraction.get_transport_data(self.CityName, transport_type, iso639_code)
        self.osm_data = application_OSM_extraction.overpass_request(self.CityName, transport_type, iso639_code)

        return len(self.osm_data)
        
    def GetTransportLineList (self):
        if (len(self.osm_data) == 0):
            return None
        ret = application_OSM_extraction.line_extraction_and_stations (self.osm_data)
        
        print (ret)
        print (type(ret))
        
        list = []
        for line in ret:
            print (line["line_name"])
            if (line["line_name"] not in list):
                list.append (line["line_name"])
        result = {"city":self.CityName, "lines":list}    
        return result
    
    def get_svg (self, linelist):
        if len (self.osm_data) == 0:
            return None
        print ("get_svg", linelist) 
        data = application_OSM_extraction.plot_get_2d_data (self.osm_data, linelist)
        
        print ("#" * 25)
        print(data)
        svg = OSMsvg.transport_data_to_svg (data)

        return str(svg)

if __name__ == "__main__":
    osm = Osmprocess()
    osm.ReadTransportData("rennes", "subway")
    ret = osm.GetLineList()
    print ('########### final ###############')
    print (ret)

    osm.get_svg()