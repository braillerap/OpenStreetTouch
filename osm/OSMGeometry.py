import cartopy.crs as ccrs
import shapely
import json
import svg
from . import OSMsvgFile
from . import OSMOrthoArea
from . import OSMSymbol
from . import OSMPath

class OsmTransportDrawing:

    def __init__(self):
        self.colors = ["#ff0000","#00ff00","#0000ff", "#ff00ff", "#00ffff", "#ffff00", "#000000", "#ff0080", "#ff8000", "#80ff00", "#00ff80", "#0080ff", "#8000ff"]
        self.colorsid = 0
        self.fill_hole = False
        self.stroke_width = 15
        self.area = None
        self.transport_lines = []
        self.showstartstation = False
        self.symbolsize = 30
        self.polygons = False
    def square_dist (self, pt1, pt2):
        """
        Calculate the squared distance between two points.

        Parameters:
        pt1 (tuple): A tuple representing the coordinates of the first point (x1, y1).
        pt2 (tuple): A tuple representing the coordinates of the second point (x2, y2).

        Returns:
        float: The squared Euclidean distance between the two points.
        """
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


    def draw_way (self, svg_file, lines, area, width, height, marginx, marginy):
        #print ("len lines", len(lines))
        for line in lines:
            if len(line["ways"]) == 0:
                continue
            if (len(line["ways"][0]["nodes"]) == 0):
                continue
            total_line = []
            start = line["ways"][0]["nodes"][0]
            
            x = round((start[0] - area.minx) * area.ratio, 2) + marginx
            y = height - round((start[1] - area.miny) * area.ratio, 2) - marginy
            cnt = 1
            
            for ways in line["ways"]:
                path = []
                if len (ways["nodes"]) == 0:
                    continue
                
                # first point in path
                # start = ways["nodes"][0]
                # x = round((start[0] - area.minx) * area.ratio, 2) + marginx
                # y = height - round((start[1] - area.miny) * area.ratio, 2) - marginy
                      
                cnt = cnt +1
                # path.append ( (x, y) )
                # total_line.append ( (x, y) )

                # next points in path                    
                for node in ways["nodes"]:
                    
                    x = round((node[0] - area.minx) * area.ratio, 2) + marginx
                    y = height - round((node[1] - area.miny) * area.ratio, 2) - marginy
                    path.append ( (x, y) )
                    total_line.append ( (x, y) )
                
                if not self.fill_hole:
                    if len(path) > 1:
                        if self.polygons:
                            fill = self.colors[self.colorsid % len(self.colors)]
                        else:
                            fill = "none"
                        tool = OSMPath.OSMPath (path)
                        
                        tool.DrawPath (svg_file, self.colors[self.colorsid % len(self.colors)], self.stroke_width, fill, self.polygons)
                    
                    # svg_file.addsvg(svg.Path(
                    #             stroke=self.colors[self.colorsid % len(self.colors)],
                    #             stroke_width=self.stroke_width,
                    #             stroke_linecap="round",
                    #             fill="none",
                    #             d=path,
                    #         ))
                    

            if len(total_line) > 1:
                # path : list[svg.Element] = []
                # path.append (svg.M (total_line[0][0], total_line[0][1]))
                
                # for node in total_line[1:]:
                #     path.append (svg.L (node[0], node[1]))
                
                if self.fill_hole:
                    if self.polygons:
                        fill = self.colors[self.colorsid % len(self.colors)]
                    else:
                        fill = "none"
                    tool = OSMPath.OSMPath (total_line)
                    tool.DrawPath (svg_file, self.colors[self.colorsid % len(self.colors)], self.stroke_width, fill, self.polygons)
                    

                    # svg_file.addsvg(svg.Path(stroke=self.colors[self.colorsid % len(self.colors)],
                    #             stroke_width=self.stroke_width,
                    #             stroke_linecap="round",
                    #             fill="none",
                    #             d=path,
                    #         ))
                    
            self.colorsid = self.colorsid + 1

    

    def build_projected_area_data (self, transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
        #proj = ccrs.Orthographic(0, 0)
        #data_proj = ccrs.PlateCarree()
        proj = ccrs.Miller()
        data_proj = ccrs.PlateCarree()
        # compute minx, miny, maxx, maxy
        self.area = OSMOrthoArea.OrthoArea ()
        lines = []
        for line in transport_2d_data:
            ways = []
            for way in line["positions_ways"]:
                nodes = []
                for node in way["nodes"]:
                    pos = proj.transform_point(node["lon"], node["lat"], data_proj)
                    
                    self.area.AddPoint (float(pos[0]), float(pos[1]))
                    self.area.AddLatLon (node["lat"], node["lon"])

                    nodes.append ( (float(pos[0]), float(pos[1]) ) )

                ways.append ({"way_id": way.get("id", "??"), "nodes":nodes})
           
            stations = []
            for station in line["stations"]:
                pos = proj.transform_point(station["lon"], station["lat"], data_proj)
                
                self.area.AddPoint (float(pos[0]), float(pos[1]))
                self.area.AddLatLon (station["lat"], station["lon"])

                stations.append({"id":station["id"], "name":station["name"], "pos":pos})
                                    
            lines.append ({"name":line["name"], "id":line["id"], "ways":ways, "stations":stations})
            
            
            

        self.area.width = self.area.maxx - self.area.minx
        self.area.height = self.area.maxy - self.area.miny
        print ("min lat", self.area.min_lat, "max lat", self.area.max_lat, 
               "min lon", self.area.min_lon, "max lon", self.area.max_lon)
        print ("minx", self.area.minx, "miny", self.area.miny, "maxx", self.area.maxx, "maxy", self.area.maxy)
        print ("width", self.area.width, "height", self.area.height)
        self.area.ratio = min ((width - 2 * marginx) / self.area.width, (height - 2 * marginy) / self.area.height)
        print ("ratio", self.area.ratio)
        
        return lines

    def get_way_square_dist (self, way1, way2, way1pos, way2pos):
        """
        Compute the square distance between two nodes on two different ways.

        Args:
            way1 (dict): The first OSM way, with a nodes list in "nodes" key.
            way2 (dict): The second way, with a nodes list in "nodes" key..
            way1pos (int): The position of the node on the first way.
            way2pos (int): The position of the node on the second way.

        Returns:
            float: The square distance between the two nodes.
        """
        if (len (way1["nodes"]) > 1):
            way1nodes = [way1["nodes"][0], way1["nodes"][-1]]
        else:
            way1nodes = [way1["nodes"][0], way1["nodes"][0]]

        if (len (way2["nodes"]) > 1):
            way2nodes = [way2["nodes"][0], way2["nodes"][-1]]
        else:
            way2nodes = [way2["nodes"][0], way2["nodes"][0]]

        return self.square_dist (way1nodes[way1pos], way2nodes[way2pos])

    def swap_transport_way (self, line):
        """
        Test and potentially swap ways given by osm in a transport line (relation).

        Args:
            line (dict): A dictionary representing a line with a list of ways.

        Returns:
            None

        """
        swap_conf = [(-1,0),(0,-1),(0,0),(-1,-1)]
        #print ("swap line", line["name"])
        if len (line["ways"]) > 1:
            prevway = line["ways"][0]
            for way in line["ways"][1:]:
                if len (way["nodes"]) <1 or len(prevway["nodes"]) < 1:
                    #print ("too short", len (way["nodes"]) ,len(prevway["nodes"]))
                    prevway = way
                    continue
                dist = []
                for conf in swap_conf:
                    #dist.append (square_dist (prevway["nodes"][conf[0]], way["nodes"][conf[1]]))
                    dist.append (self.get_way_square_dist (prevway, way, conf[0], conf[1]))
                    
                minv = dist[0]
                minp = 0
                
                for i in range (1, len (dist)):
                    if dist[i] < minv:
                        minv = dist[i]
                        minp = i
                
                if minp == 0:
                    # all seem good
                    pass
                elif minp == 1:
                    # swap 0,1
                    prevway["nodes"].reverse ()
                    way["nodes"].reverse ()
                    pass
                elif minp == 2:
                    # swap 0
                    prevway["nodes"].reverse ()
                    pass    
                elif minp == 3:
                    # swap 1
                    way["nodes"].reverse ()
                    pass
                #print(minp)
                prevway = way
                

    def build_projected_data (self, transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
        self.transport_lines = self.build_projected_area_data (transport_2d_data, width, height, marginx, marginy)

    def build_station (self, fsvg, position, symbol, strokecolor, fillcolor, width, height, marginx, marginy):
        symbolengine = OSMSymbol.OSMSymbol ()
        x = round((position[0] - self.area.minx) * self.area.ratio, 2) + marginx
        y = height - round((position[1] - self.area.miny) * self.area.ratio, 2) - marginy
                    
        symbolengine.DrawSymbol (fsvg, symbol, x, y, self.symbolsize, fillcolor, strokecolor)                        
        
    def build_stations (self, fsvg, width=1000, height=1000, marginx= 50, marginy=50):
        
        for line in self.transport_lines:
            if "stations" in line:
                stations = line["stations"]
                
                if len (stations) > 2:
                    start = stations[0]
                    end = stations[-1]

                    self.build_station (fsvg, start["pos"], OSMSymbol.OSMSymbolType.Square, self.colors[self.colorsid % len(self.colors)], self.colors[self.colorsid % len(self.colors)], width, height, marginx, marginy)
                    self.build_station (fsvg, end["pos"], OSMSymbol.OSMSymbolType.Triangle, self.colors[self.colorsid % len(self.colors)], self.colors[self.colorsid % len(self.colors)], width, height, marginx, marginy)

                    for station in stations[1:-1]:
                       
                        self.build_station (fsvg, station["pos"], OSMSymbol.OSMSymbolType.Circle, self.colors[self.colorsid % len(self.colors)], self.colors[self.colorsid % len(self.colors)], width, height, marginx, marginy)    
                else:   
                    for station in stations:
                        self.build_station (fsvg, station["pos"], OSMSymbol.OSMSymbolType.Circle, self.colors[self.colorsid % len(self.colors)], self.colors[self.colorsid % len(self.colors)], width, height, marginx, marginy)
                        

                self.colorsid += 1

    def build_poly_from_ways (self, fsvg, width=1000, height=1000, marginx= 50, marginy=50):
        for line in self.transport_lines:
            self.swap_transport_way (line)
        self.draw_way (fsvg, self.transport_lines, self.area, width, height, marginx, marginy)
        
    def build_poly_from_stations (self, fsvg, width=1000, height=1000, marginx= 50, marginy=50):
        self.colorsid = 0
        
        for line in self.transport_lines:
            positions = []
            for station in line["stations"]:
                pos = station["pos"]
                x = round((pos[0] - self.area.minx) * self.area.ratio, 2) + marginx
                y = height - round((pos[1] - self.area.miny) * self.area.ratio, 2) - marginy
                positions.append ((x,y))
                
            if len(positions) > 1:
                path : list[svg.Element] = []
                path.append (svg.M (positions[0][0], positions[0][1]))
                for pos in positions[1:]:
                    path.append (svg.L (pos[0], pos[1]))
                fsvg.addsvg(svg.Path(
                                stroke=self.colors[self.colorsid % len(self.colors)],
                                stroke_width=self.stroke_width,
                                stroke_linecap="round",
                                fill="none",
                                d=path,
                            ))
            self.colorsid += 1
        
class OSMStreetDrawing:
    def __init__(self):
        self.area = None
        self.color = "#ff0000"
        self.stroke_width = 2
        self.fill = "none"
        self.geoposition = (0,0)
        self.roadcolor = "#408040"
        self.footcolor = "#00ff00"
        self.footway_tags = ["footway","path", "cycleway", "steps"]

    def GetColorCategory (self, tags):
        if 'highway' in tags:
            if tags['highway'] in self.footway_tags:
                return   self.footcolor
            else:
                return self.roadcolor
        return self.color
    
    def EstimateStreetWidth (self, tags):
        categories = {
            "motorway":11, 
            "motorway-link":9, 
            "motorway_link":9, 
            "trunk":11,
            "trunk-link":9,
            "trunk_link":9,
            "primary":11, 
            "primary-link":9,
            "primary_link":9,
            "secondary":9, 
            "secondary-link":7, 
            "secondary_link":7, 
            "tertiary":7, 
            "tertiary-link":5, 
            "tertiary_link":5, 
            "residential":5,
            "living-street":5,
            "living_street":5,
            "pedestrian":4,
            "road":7,
            "service":7,
            "minor-service":5,
            "minor_service":5,
            "footway":2,
            "path":2,
            "cycleway":2,
            "steps":2.5,
            }
        if 'footpath' in tags:
            print ("detected footpath")
        if 'highway' in tags:
            
            if tags['highway'] in categories:
                
                return categories[tags['highway']]
            else:
                print (tags["highway"], "not classified")
        return 4
    
    def filter_footpath (self, ways):
        footways = []
        for way in ways:
            if 'highway' in way['tags']:
                if way['tags']['highway'] in self.footway_tags:
                    footways.append (way)
        return footways
    
    def build_projected_area_data (self, street_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
        #proj = ccrs.Orthographic(self.geoposition[0], self.geoposition[1])
        proj = ccrs.Miller()
        data_proj = ccrs.PlateCarree()
        #data_proj = ccrs.Miller()
        #json.dump (street_2d_data, open ("street_2d_data.json", "w"), indent=4)

        # compute minx, miny, maxx, maxy
        self.area = OSMOrthoArea.OrthoArea ()
        
        
        streets = []
        buildings = []
        unclassified = []
        for way in street_2d_data["street"]:
            swidth = self.EstimateStreetWidth (way['tags'])
            nodes = []
            for node in way["nodes"]:
                #print (node)
                pos = proj.transform_point(node["lon"], node["lat"], data_proj)
                
                self.area.AddPoint (float(pos[0]), float(pos[1]))
                self.area.AddLatLon (node["lat"], node["lon"])
                
                nodes.append ( (float(pos[0]), float(pos[1]) ) )
            streets.append ({"way_id": way.get("id", "??"), "street_width":swidth, "nodes":nodes, "tags": way['tags']})
        
        for way in street_2d_data["building"]:
            nodes = []
            for node in way["nodes"]:
                
                pos = proj.transform_point(node["lon"], node["lat"], data_proj)
                
                self.area.AddPoint (float(pos[0]), float(pos[1]))
                self.area.AddLatLon (node["lat"], node["lon"])

                nodes.append ( (float(pos[0]), float(pos[1]) ) )

            buildings.append ({"way_id": way.get("id", "??"), "nodes":nodes})                        
        
        for way in street_2d_data["unclassified"]:
            nodes = []
            for node in way["nodes"]:
                
                pos = proj.transform_point(node["lon"], node["lat"], data_proj)
                
                self.area.AddPoint (float(pos[0]), float(pos[1]))
                self.area.AddLatLon (node["lat"], node["lon"])

                nodes.append ( (float(pos[0]), float(pos[1]) ) )

            unclassified.append ({"way_id": way.get("id", "??"), "nodes":nodes})    
            
            

        self.area.width = self.area.maxx - self.area.minx
        self.area.height = self.area.maxy - self.area.miny
        print ("min lat", self.area.min_lat, "max lat", self.area.max_lat, 
            "min lon", self.area.min_lon, "max lon", self.area.max_lon)
        print ("minx", self.area.minx, "miny", self.area.miny, "maxx", self.area.maxx, "maxy", self.area.maxy)
        print ("width", self.area.width, "height", self.area.height)
        self.area.ratio = min ((width - 2 * marginx) / self.area.width, (height - 2 * marginy) / self.area.height)
        print ("ratio", self.area.ratio)
        
        return {"streets": streets, "buildings": buildings, "unclassified": unclassified}
    
    def draw_poly_ways (self, fsvg, waysnode, width, height, marginx, marginy):
        for way in waysnode:
            path : list[svg.Element] = []
            
            swidth = way.get ("street_width", 1)
            realwidth = swidth 
            color = self.GetColorCategory (way["tags"])
            fill = "none"

            
            if len (way["nodes"]) > 1:
                # line = shapely.LineString(way["nodes"])
                
                # offseted = shapely.buffer(line, realwidth/2, cap_style='square', join_style='bevel')
                # polypts = shapely.get_coordinates(offseted)
                path = []
                for node in way["nodes"]:
                    x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                    y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                    path.append ( (x, y) )
                
                tool = OSMPath.OSMPath (path)
                tool.DrawPath (fsvg, color, realwidth, color, True)
                    
                
                # if len (polypts) > 0:
                #     node = polypts[0]
                #     x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                #     y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                #     path.append (svg.M (x, y))
                    
                #     for node in polypts[1:]:
                #         x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                #         y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                #         path.append (svg.L (x, y))
                    
                #     # add first node to close the path
                #     node = polypts[0]
                #     x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                #     y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                #     path.append (svg.L (x, y))

                #     fsvg.addsvg(
                #         svg.Path(
                #             stroke=color,
                #             stroke_width=0.1,
                #             stroke_linecap="round",
                #             fill=color,
                #             d=path,
                #     ))

    def draw_width_ways (self, fsvg, waysnode, width, height, marginx, marginy):
        for way in waysnode:
            path =[]
            
            swidth = way.get ("street_width", 1)
            realwidth = swidth * self.area.ratio 
            
            color = self.GetColorCategory (way["tags"])
            fill = "none"

           
            if len (way["nodes"]) > 1:
                for node in way["nodes"]:
                     x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                     y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                     path.append ( (x, y) )
                   
                tool = OSMPath.OSMPath (path)
                tool.DrawPath (fsvg, color, realwidth,  fill, False)
            
                # node = way["nodes"][0]
                # x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                # y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                # path.append (svg.M (x, y))
                # for node in way["nodes"][1:]:
                #     x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                #     y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                #     path.append (svg.L (x, y))

                # fsvg.addsvg(
                #     svg.Path(
                #         stroke=color,
                #         stroke_width=realwidth,
                #         stroke_linecap="round",
                #         fill=fill,
                #         d=path,
                # ))

    def draw_ways (self, fsvg, waysnode, width, height, marginx, marginy):
        for ways in waysnode:
            path = []
            
            if len (ways["nodes"]) > 1:
                
                for node in ways["nodes"]:
                    x = round((node[0] - self.area.minx) * self.area.ratio, 2) + marginx
                    y = height - round((node[1] - self.area.miny) * self.area.ratio, 2) - marginy
                    path.append ( (x, y) )
                tool = OSMPath.OSMPath (path)
                tool.DrawPath (fsvg, self.color, self.stroke_width, self.fill, False)
                    
                # fsvg.addsvg(
                #     svg.Path(
                #         stroke=self.color,
                #         stroke_width=self.stroke_width,
                #         stroke_linecap="round",
                #         fill=self.fill,
                #         d=path,
                # ))


    def build_projected_data (self, transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
        self.street2d_data = self.build_projected_area_data (transport_2d_data, width, height, marginx, marginy)

    def DrawingStreetMap (self, fsvg, street_2d_data, width=1000, height=1000, marginx= 50, marginy=50, building=True, footpath=False, polygon=False):
        
        
        waysnode = self.build_projected_area_data (street_2d_data, width, height, marginx, marginy)
        
        #print (waysnode)
        # Draw the ways using the fsvg, waysnode, width, height, marginx, and marginy parameters
        
        print (len(waysnode["buildings"]), len(waysnode["streets"]), len(waysnode["unclassified"]))
        print ("building", building, "footpath", footpath, "polygon", polygon)

        if building:
            self.color = "blue"
            self.stroke_width = 0.1
            self.fill = "lightblue"
            self.draw_ways (fsvg, waysnode["buildings"], width, height, marginx, marginy)

        self.color = "green"
        #self.stroke_width = 3
        self.fill = "none"
        print (polygon)
        if footpath:
            footpath = self.filter_footpath (waysnode["streets"])
            if polygon:
                self.draw_poly_ways (fsvg, footpath, width, height, marginx, marginy)
            else:    
                self.draw_width_ways (fsvg, footpath, width*20, height, marginx, marginy)
        else:    
            if polygon:
                self.draw_poly_ways (fsvg, waysnode["streets"], width, height, marginx, marginy)  
            else:  
                self.draw_width_ways (fsvg, waysnode["streets"], width*20, height, marginx, marginy)
        
        
        self.color = "red"
        self.stroke_width = 3
        self.fill = "none"
        #self.draw_ways (fsvg, waysnode["unclassified"], width, height, marginx, marginy)
        
        
