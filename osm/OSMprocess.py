from . import application_OSM_extraction 
from . import OSMsvg
import pandas as pd

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
        
        # build selected lines list
        desired_lines = [trline["name"] for trline in linelist if trline["select"] == True]

        print ("desired lines :" , desired_lines)                
        #data = application_OSM_extraction.plot_get_2d_data (self.osm_data, linelist)
        #data = application_OSM_extraction.lines_ways_extraction_from_datta (self.osm_data)
        data = self.lines_ways_extraction_from_data_filtered(self.osm_data, desired_lines)
        # naive filtering panda dataframe
        #df = data.copy ()
        #df = df[df["line_name"].isin(desired_lines)]
        
        print ("#" * 25)
        print(data)
        print (type(data))
        #svg = OSMsvg.transport_data_to_svg (data)

        return str(svg)


    def lines_ways_extraction_from_data_filtered(self, data, linelist): # => ok 
        """
        ways extraction of list of transportation lines from data produced by overpass request.
        
        this function extracts ways associated to each relation describing a transportation line. 
        the returned dataframe permits to create a map of the network based on real wyas of the lines. 
        this dataframe contains nodes latitudes and longitudes.
        
        param : 
        -------
            data : OSM data extracted with overpass request 
            
        returns :
        ---------
            df_line_tracks : pandas dataframe containing ways description of each extracted line relation.
                            columns : ['line_name', 'way_id', 'public_transport', 'latitude', 'longitude']
                            "latitude" and "longitude" are the coordonates of each node of the considered way
                            
                            Note : this function calls lines_list_extraction_from_data(data)  
        """

        #global relations, nodes, ways
        #global relation, way, node  
        #global dic_line_segments 
        
        # relations, ways, and nodes extraction from data 
        relations = {element['id']: element for element in data['elements'] if element['type'] == 'relation'}
        nodes = {element['id']: element for element in data['elements'] if element['type'] == 'node'}
        ways = [element for element in data['elements'] if element['type'] == 'way']
        
        print ("relations", relations)
        # group by relation (line id)
        dic_line_segments = {}
        
        # get line list 
        df_line_list = application_OSM_extraction.lines_list_extraction_from_data(data) 
        print ("df_line_list", df_line_list)
        print ("df_line_list.keys", df_line_list.keys())
        print ("df_line_list.columns", df_line_list.columns)
        col = df_line_list.keys()
        for key in col:
            print (key, df_line_list.at[0, key])
        # loop on ways 
        for way in ways:
            #print("Way ID : ", way['id'], " - ", way.keys()) 
            
            # get line name in way attributes 
            line_name = way.get('tags', {}).get('name', 'Unknown line')
            way_id = way['id'] 
            way_public_transport = way.get('tags', {}).get('public_transport', 'Unknown')
            #if line_name not in linelist:
            #    print ("===> reject :", line_name)
            #    continue
            
            #print ("===> accept :", line_name)
            
            # is it a new way ?
            if way_id not in dic_line_segments:
                dic_line_segments[way_id] = {
                    "line_name": line_name,
                    "way_id": way_id,
                    "public_transport": way_public_transport, 
                    "coordinates": []
                }
            
            # get nodes coordonnates 
            coordinates = []
            # analysis of nodes list contained in the way 
            for node_id in way.get('nodes', []):
                # get node data from it's id  
                node = nodes.get(node_id)
                if node:
                    # add node coordinnates 
                    coordinates.append((node['lat'], node['lon']))
            
            # add to dictionnary 
            dic_line_segments[way_id]["coordinates"].extend(coordinates)
        
        # convert dic to DataFrame
        #print ("*" * 25)
        #print ("info", dic_line_segments)
        df_line_tracks = pd.DataFrame.from_records([
            {"line_name": info["line_name"], "way_id": info["way_id"], "public_transport": info["public_transport"],  "coordinates": info["coordinates"]}
            for info in dic_line_segments.values()
        ])
        print (df_line_tracks)
        
        # create latitude and logitude columns from coordinaites 
        # Extraction of nodes listes latitude and longitudes
        df_line_tracks['latitude'] = df_line_tracks['coordinates'].apply(lambda coords: [point[0] for point in coords])
        df_line_tracks['longitude'] = df_line_tracks['coordinates'].apply(lambda coords: [point[1] for point in coords])
        
        # delete coordinates column  
        df_line_tracks = df_line_tracks.drop(columns=['coordinates'])
        
        return df_line_tracks 

if __name__ == "__main__":
    osm = Osmprocess()
    osm.ReadTransportData("rennes", "subway")
    ret = osm.GetLineList()
    print ('########### final ###############')
    print (ret)

    osm.get_svg()