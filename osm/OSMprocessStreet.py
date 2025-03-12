from . import application_OSM_extraction 
from . import OSMsvg
from . import OSMGeometry
from . import OSMTransitInfo
from . import OSMsvgFile
from . import OSMStreetMap

import json

class OSMprocessStreet:
    def __init__(self):
        self.streetmap_data = None
        self.radius = 0
        self.geoposition = (0, 0)
    

    def ReadStreetMapData (self, lat, lon, radius):
        # Get the street map data from the Overpass API
        self.streetmap_data = OSMStreetMap.overpass_request (lat, lon, radius)
         
        # Extract the map from the street map data
        map = OSMStreetMap.osm_extraction (self.streetmap_data)

        street_2d_data = OSMStreetMap.osm_extract_data (map)
        self.radius = int(radius)
        self.geoposition = (lat, lon)

        return (street_2d_data)
    
    def GetStreetMapSVG (self, street_data, lat=0, lon=0, building=True, footpath=False, polygon=False, includeWater=False, cliping=False):
        width = 1000
        height = 1000
        marginx = 50
        marginy = 50

        fsvg = OSMsvgFile.OSMsvgFile ()
        fsvg.open (widthmm=width, heightmm=height)
        
        engine = OSMGeometry.OSMStreetDrawing ()
        engine.radius = self.radius
        engine.geoposition = self.geoposition
        engine.clipdata = cliping
        engine.DrawingStreetMap (fsvg, street_data, width, height, marginx, marginy, building, footpath, polygon, includeWater)

        fsvg.close ()
        return (fsvg.getSVGString())

if __name__ == "__main__":
    osm = OSMprocessStreet()
    ret = osm.ReadStreetMapData("rennes", "subway")
   
    print ('########### final ###############')
    print (ret)

   