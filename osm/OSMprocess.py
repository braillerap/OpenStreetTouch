from . import application_OSM_extraction 
from . import OSMsvg

class Osmprocess:
    def __init__(self):
        self.osm_data = None
        self.CityName =""

    def ReadTransportData (self, city, transport_type, iso639_code = "fr"):
        # todo : check capitals in name
        self.CityName = city.title()
        self.osm_data = application_OSM_extraction.get_transport_data(self.CityName, transport_type, iso639_code)
        
        return self.osm_data.size 
        
    def GetTransportLineList (self):
        if (self.osm_data.size == 0):
            return None
        ret = application_OSM_extraction.get_line_list (self.osm_data)
        
        print (ret)
        print (type(ret))

        tmp = ret.to_dict ()
        print ("as dict")
        print (tmp)

        result = {"city":self.CityName, "lines":tmp}    
        return result
    
    def get_svg (self):
        if (self.osm_data.size == 0):
            return None
         
        data = application_OSM_extraction.plot_get_2d_data (self.osm_data)
        
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