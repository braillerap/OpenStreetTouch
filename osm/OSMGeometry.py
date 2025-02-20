import utm
import cartopy.crs as ccrs
import json
import svg
from . import OSMsvgFile
from . import OSMOrthoArea


def square_dist (pt1, pt2):
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def draw_way (svg_file, lines, area, width, height, marginx, marginy):
   
    colors=["#ff0000","#00ff00","#0000ff"]
    colorid = 0
    print ("len lines", len(lines))
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
            path : list[svg.Element] = []
            if len (ways["nodes"]) == 0:
                continue
            
            start = ways["nodes"][0]
            x = round((start[0] - area.minx) * area.ratio, 2) + marginx
            y = height - round((start[1] - area.miny) * area.ratio, 2) - marginy
            svg_file.addsvg (svg.Circle(cx=x, cy=y, r=10, fill="#00ff0040"))
            svg_file.addsvg(
                   svg.Text(x=x, y=y -10 -cnt / 2, class_=["small"], text=str(cnt))
                   )
            cnt = cnt +1
            path.append (svg.M (x, y))
            total_line.append ((x, y))
            for node in ways["nodes"][1:]:
                
                x = round((node[0] - area.minx) * area.ratio, 2) + marginx
                y = height - round((node[1] - area.miny) * area.ratio, 2) - marginy
                path.append (svg.L (x, y))
                total_line.append ((x, y))

            # svg_file.addsvg(svg.Path(
            #                 stroke=colors[colorid % len(colors)],
            #                 stroke_width=3,
            #                 stroke_linecap="round",
            #                 fill="none",
            #                 d=path,
            #             ))
            colorid += 1

        if len(total_line) > 1:
            path : list[svg.Element] = []
            path.append (svg.M (total_line[0][0], total_line[0][1]))
            #svg_file.addsvg (svg.Circle(cx=x, cy=y, r=20, fill="#ff000040"))
            for node in total_line[1:]:
                path.append (svg.L (node[0], node[1]))
            
            svg_file.addsvg(svg.Path(stroke="#00000040",
                        stroke_width=8,
                        stroke_linecap="round",
                        fill="none",
                        d=path,
                    ))

def build_area_data (transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
    proj = ccrs.Orthographic(0, 0)
    data_proj = ccrs.PlateCarree()

    # compute minx, miny, maxx, maxy
    area = OSMOrthoArea.OrthoArea ()
    lines = []
    for line in transport_2d_data:
        ways = []
        for way in line["positions_ways"]:
            nodes = []
            for node in way["nodes"]:
                pos = proj.transform_point(node["lon"], node["lat"], data_proj)
                
                area.minx = min ([area.minx, float(pos[0])])
                area.miny = min ([area.miny, float (pos[1])])
                area.maxx = max ([area.maxx, float (pos[0])])
                area.maxy = max ([area.maxy, float (pos[1])])
                
                area.min_lat = min([area.min_lat, node["lat"]])
                area.max_lat = max([area.max_lat, node["lat"]])
                area.min_lon = min([area.min_lon, node["lon"]])
                area.max_lon = max([area.max_lon, node["lon"]])
                
                nodes.append ( (float(pos[0]), float(pos[1]) ) )
            ways.append ({"way_id": way.get("id", "??"), "nodes":nodes})
        
        lines.append ({"name":line["name"], "id":line["id"], "ways":ways})
                
        

    area.width = area.maxx - area.minx
    area.height = area.maxy - area.miny
    print ("min lat", area.min_lat, "max lat",area. max_lat, "min lon", area.min_lon, "max lon", area.max_lon)
    print ("minx", area.minx, "miny", area.miny, "maxx", area.maxx, "maxy", area.maxy)
    print ("width", area.width, "height", area.height)
    area.ratio = min ((width - 2 * marginx) / area.width, (height - 2 * marginy) / area.height)
    print ("ratio", area.ratio)
    
    return area,lines

def test_swap (line):
    swap_conf = [(-1,0),(0,-1),(0,0),(-1,-1)]
    print ("swap line", line["name"])
    if len (line["ways"]) > 1:
        
        
        prevway = line["ways"][0]
        for way in line["ways"][1:]:
            if len (way["nodes"]) <2 or len(prevway["nodes"]) < 2:
                print ("too short", len (way["nodes"]) ,len(prevway["nodes"]))
                prevway = way
                continue
            dist = []
            for conf in swap_conf:
                
                dist.append (square_dist (prevway["nodes"][conf[0]], way["nodes"][conf[1]]))
            minv = dist[0]
            minp = 0
            
            for i in range (1, len (dist)):
                if dist[i] < minv:
                    minv = dist[i]
                    minp = i
            print ("minp", minp, "dist", minv)
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
            print(minp)
            prevway = way
            

def build_poly_from_ways (transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):

    area,lines = build_area_data (transport_2d_data, width, height, marginx, marginy)

    for line in lines:
        test_swap (line)

    fsvg = OSMsvgFile.OSMsvgFile ()
    fsvg.open (widthmm=width, heightmm=height)
    draw_way (fsvg, lines, area, width, height, marginx, marginy)
    fsvg.close ()
    fsvg.writeToFile ("test3.svg")

    return fsvg.getSVG ()