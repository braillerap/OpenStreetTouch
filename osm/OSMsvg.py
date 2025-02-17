import svg
from textwrap import dedent
import utm
import cartopy.crs as ccrs


def square_dist (pt1, pt2):
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
def reorder_path_for_nearest (pos, path):
    if len(path) > 1:
        diststart = square_dist (pos, path[0])
        distend = square_dist (pos, path[-1])
        if diststart > distend:
            path.reverse()
    return path
def transport_data_to_svg_from_dicways (transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
    
    draw_labels = False
    drawmiddle = True
    proj = ccrs.Orthographic(0, 0)
    data_proj = ccrs.PlateCarree()

    # build the square area for offset and ration
    minx = 100000000
    miny = 100000000
    maxx = -100000000
    maxy = -100000000
    min_lat = 100000000
    max_lat = -100000000
    min_lon = 100000000
    max_lon = -100000000
    colors = ("red","black","blue")
    color_id = 0
    
    for line in transport_2d_data:
        print ("line", line["name"])
        for position in line["positions_dic"]:
                      
            pos = proj.transform_point(position["lon"], position["lat"], data_proj)
            #pos = utm.from_latlon(station["lat"], station["long"])
            minx = min ([minx, pos[0]])
            miny = min ([miny, pos[1]])
            maxx = max ([maxx, pos[0]])
            maxy = max ([maxy, pos[1]])

            min_lat = min([min_lat, position["lat"]])
            max_lat = max([max_lat, position["lat"]])
            min_lon = min([min_lon, position["lon"]])
            max_lon = max([max_lon, position["lon"]])

    sizex = maxx - minx
    sizey = maxy - miny
    print ("min lat", min_lat, "max lat", max_lat, "min lon", min_lon, "max lon", max_lon)
    print ("minx", minx, "miny", miny, "maxx", maxx, "maxy", maxy)
    
    ratio = min ((width - 2 * marginx) / sizex, (height - 2 * marginy) / sizey)
    print ("ratio", ratio)
    
    # build dvg graph
    elements: list[svg.Element] = []
    elements.append (
        svg.Style(
                text=dedent("""
                    .small { font: 10px sans-serif; }
                    .smallred { font: 10px sans-serif; fill:red}
                    .heavy { font: bold 30px sans-serif; }

                    /* Note that the color of the text is set with the    *
                    * fill property, the color property is for HTML only */
                    .Rrrrr { font: italic 40px serif; fill: red; }
                """),
            ),
    )
    
    
    for line in transport_2d_data:
        print ("svg drawing line", line["name"])
        cnt = 0
        previous_pos = None
        lastway_position = None
        total_pos = []
        for way in line["positions_ways"]:
            transport_line_pos = []
            for position in way["nodes"]:
                pos = proj.transform_point(position["lon"], position["lat"], data_proj)
                #print (pos)
                x = round((pos[0] - minx) * ratio, 2) + marginx
                y = height - round((pos[1] - miny) * ratio, 2) - marginy
                
                transport_line_pos.append( (x,y) )
                
                lastway_position = (x,y)

            if previous_pos:
                reorder_path_for_nearest (previous_pos, transport_line_pos)
            previous_pos = lastway_position
            
            for tpos in transport_line_pos:
                total_pos.append ( tpos)
            
            path : list[svg.element] = []
            if len(transport_line_pos) > 0:
                path.append (svg.M(transport_line_pos[0][0],transport_line_pos[0][1]))

            for pos in transport_line_pos[1:]:    
                #print (pos[0],pos[1])    
                path.append (svg.L(pos[0],pos[1]))
            
            elements.append(svg.Path(
                        stroke=colors[color_id],
                        stroke_width=1,
                        stroke_linecap="round",
                        fill="none",
                        d=path,
                    ))

            # find way middle
            if drawmiddle and len (way["nodes"]) > 1:
                pos = proj.transform_point(way["nodes"][0]["lon"], way["nodes"][0]["lat"], data_proj)
                x1 = round((pos[0] - minx) * ratio, 2) + marginx
                y1 = height - round((pos[1] - miny) * ratio, 2) - marginy
                pos = proj.transform_point(way["nodes"][-1]["lon"], way["nodes"][-1]["lat"], data_proj)
                x2 = round((pos[0] - minx) * ratio, 2) + marginx
                y2 = height - round((pos[1] - miny) * ratio, 2) - marginy
                path : list[svg.element] = []
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                path.append (svg.M(x,y))
                path.append (svg.L(x+10, y -10))
                elements.append(svg.Path(
                        stroke="pink",
                        stroke_width=1,
                        stroke_linecap="round",
                        fill="none",
                        d=path,
                    ))
                elements.append(
                    svg.Text(x=x+10, y=y -10, class_=["smallred"], text=str(cnt))
                    )
                cnt += 1
            color_id += 1
            if color_id >= len(colors):
                color_id = 0
    
        path : list[svg.element] = []
        if len(total_pos) > 0:
            path.append (svg.M(total_pos[0][0],total_pos[0][1]))

        for pos in total_pos[1:]:    
            #print (pos[0],pos[1])    
            path.append (svg.L(pos[0],pos[1]))
        
        elements.append(svg.Path(
                    stroke="#ffff0080",
                    stroke_width=9,
                    stroke_linecap="round",
                    fill="none",
                    d=path,
                ))
    # build labels
    if draw_labels:
        label =""
        for line in transport_2d_data:
            for position in line["positions_dic"]:
                if str(position["way_id"]) != label:
                    label = str(position["way_id"])
                    pos = proj.transform_point(position["lon"], position["lat"], data_proj)
                    #print (pos)
                    x = round((pos[0] - minx) * ratio, 2) + marginx
                    y = height - round((pos[1] - miny) * ratio, 2) - marginy
                    xl = x + 20
                    yl = y
                    print (x,y, label)
                    path : list[svg.element] = []
                    path.append (svg.M(x,y))
                    path.append (svg.L(xl,yl))
                    elements.append(svg.Path(
                        stroke="#00ff00",
                        stroke_width=1,
                        stroke_linecap="round",
                        fill="none",
                        d=path,
                    ))
                    elements.append(
                    svg.Text(x=xl, y=yl, class_=["small"], text=label + " " + str(position["route"]) + " " + str(position["id"]))
                    )

    fig = svg.SVG(
                viewBox=svg.ViewBoxSpec(0, 0, width, height),
                width=svg.mm(width),
                height=svg.mm(height),
                elements=elements
                )
    with open('test.svg', 'w') as f:
        f.write(str(fig))
    return fig
def transport_data_to_svg_from_dic (transport_2d_data, width=1000, height=1000, marginx= 50, marginy=50):
    

    proj = ccrs.Orthographic(0, 0)
    data_proj = ccrs.PlateCarree()

    # build the square area for offset and ration
    minx = 100000000
    miny = 100000000
    maxx = -100000000
    maxy = -100000000
    min_lat = 100000000
    max_lat = -100000000
    min_lon = 100000000
    max_lon = -100000000
    
    for line in transport_2d_data:
        print ("line", line["name"])
        for position in line["positions_dic"]:
                      
            pos = proj.transform_point(position["lon"], position["lat"], data_proj)
            #pos = utm.from_latlon(station["lat"], station["long"])
            minx = min ([minx, pos[0]])
            miny = min ([miny, pos[1]])
            maxx = max ([maxx, pos[0]])
            maxy = max ([maxy, pos[1]])

            min_lat = min([min_lat, position["lat"]])
            max_lat = max([max_lat, position["lat"]])
            min_lon = min([min_lon, position["lon"]])
            max_lon = max([max_lon, position["lon"]])

    sizex = maxx - minx
    sizey = maxy - miny
    print ("min lat", min_lat, "max lat", max_lat, "min lon", min_lon, "max lon", max_lon)
    print ("minx", minx, "miny", miny, "maxx", maxx, "maxy", maxy)
    
    ratio = min ((width - 2 * marginx) / sizex, (height - 2 * marginy) / sizey)
    print ("ratio", ratio)
    
    # build dvg graph
    elements: list[svg.Element] = []
    elements.append (
        svg.Style(
                text=dedent("""
                    .small { font: italic 13px sans-serif; }
                    .heavy { font: bold 30px sans-serif; }

                    /* Note that the color of the text is set with the    *
                    * fill property, the color property is for HTML only */
                    .Rrrrr { font: italic 40px serif; fill: red; }
                """),
            ),
    )

    for line in transport_2d_data:
        print ("line", line["name"])
        transport_line_pos = []
        for position in line["positions_dic"]:
            pos = proj.transform_point(position["lon"], position["lat"], data_proj)
            #print (pos)
            x = round((pos[0] - minx) * ratio, 2) + marginx
            y = height - round((pos[1] - miny) * ratio, 2) - marginy
            print (x,y)
            transport_line_pos.append( (x,y) )
        path : list[svg.element] = []
        if len(transport_line_pos) > 0:
            path.append (svg.M(transport_line_pos[0][0],transport_line_pos[0][1]))

        for pos in transport_line_pos[1:]:    
            #print (pos[0],pos[1])    
            path.append (svg.L(pos[0],pos[1]))
        
        elements.append(svg.Path(
                    stroke="#ff0000",
                    stroke_width=1,
                    stroke_linecap="round",
                    fill="none",
                    d=path,
                ))

    # build labels
    label =""
    for line in transport_2d_data:
        for position in line["positions_dic"]:
            if str(position["way_id"]) != label:
                label = str(position["way_id"])
                pos = proj.transform_point(position["lon"], position["lat"], data_proj)
                #print (pos)
                x = round((pos[0] - minx) * ratio, 2) + marginx
                y = height - round((pos[1] - miny) * ratio, 2) - marginy
                xl = x + 20
                yl = y
                print (x,y, label)
                path : list[svg.element] = []
                path.append (svg.M(x,y))
                path.append (svg.L(xl,yl))
                elements.append(svg.Path(
                    stroke="#00ff00",
                    stroke_width=1,
                    stroke_linecap="round",
                    fill="none",
                    d=path,
                ))
                elements.append(
                svg.Text(x=xl, y=yl, class_=["small"], text=label + " " + str(position["route"]) + " " + str(position["id"]))
                )

    fig = svg.SVG(
                viewBox=svg.ViewBoxSpec(0, 0, width, height),
                width=svg.mm(width),
                height=svg.mm(height),
                elements=elements
                )
    with open('test.svg', 'w') as f:
        f.write(str(fig))
    return fig
def transport_data_to_svg2 (transport_2d_data, width=1000, height=1000):
    

    proj = ccrs.Orthographic(0, 0)
    data_proj = ccrs.PlateCarree()

    # build the square area for offset and ration
    minx = 100000000
    miny = 100000000
    maxx = -100000000
    maxy = -100000000
    min_lat = 100000000
    max_lat = -100000000
    min_lon = 100000000
    max_lon = -100000000
    
    for line in transport_2d_data:
        print ("line", line["name"])
        for position in line["positions_dic"]:
                      
            pos = proj.transform_point(position[1], position[0], data_proj)
            #pos = utm.from_latlon(station["lat"], station["long"])
            minx = min ([minx, pos[0]])
            miny = min ([miny, pos[1]])
            maxx = max ([maxx, pos[0]])
            maxy = max ([maxy, pos[1]])

            min_lat = min([min_lat, position[0]])
            max_lat = max([max_lat, position[0]])
            min_lon = min([min_lon, position[1]])
            max_lon = max([max_lon, position[1]])

    sizex = maxx - minx
    sizey = maxy - miny
    print ("min lat", min_lat, "max lat", max_lat, "min lon", min_lon, "max lon", max_lon)
    print ("minx", minx, "miny", miny, "maxx", maxx, "maxy", maxy)
    
    ratio = min (width / sizex, height / sizey)
    print ("ratio", ratio)
    
    # build dvg graph
    elements: list[svg.Element] = []

    for line in transport_2d_data:
        print ("line", line["name"])
        transport_line_pos = []
        for position in line["positions"]:
            pos = proj.transform_point(position[1], position[0], data_proj)
            #print (pos)
            x = round((pos[0] - minx) * ratio, 2)
            y = height - round((pos[1] - miny) * ratio, 2)
            print (x,y)
            transport_line_pos.append( (x,y) )
        path : list[svg.element] = []
        if len(transport_line_pos) > 0:
            path.append (svg.M(transport_line_pos[0][0],transport_line_pos[0][1]))

        for pos in transport_line_pos[1:]:    
            #print (pos[0],pos[1])    
            path.append (svg.L(pos[0],pos[1]))
        
        elements.append(svg.Path(
                    stroke="#ff0000",
                    stroke_width=1,
                    stroke_linecap="round",
                    fill="none",
                    d=path,
                ))
        
    fig = svg.SVG(
                viewBox=svg.ViewBoxSpec(0, 0, width, height),
                width=svg.mm(width),
                height=svg.mm(height),
                elements=elements
                )
    with open('test.svg', 'w') as f:
        f.write(str(fig))
    return fig

def transport_data_to_svg (transport_2d_data, width=1000, height=1000):
    elm: list[svg.Element] = []

    station_utm = []
    """
                    "station_order": linedata['station_order'][keys], 
                    "name": linedata['station_name'][keys],
                    "lat": linedata['latitude [deg]'][keys],
                    "long": linedata['longitude [deg]'][keys],
                    "crossing": linedata['crossing'][keys]
    """
    proj = ccrs.Orthographic(0, 0)
    data_proj = ccrs.PlateCarree()
    for line in transport_2d_data:
        for station in line["stations"]:
            stat = station.copy()

            
            pos = proj.transform_point(station["long"], station["lat"], data_proj)
            #pos = utm.from_latlon(station["lat"], station["long"])
            stat["x"] = pos[0]
            stat["y"] = pos[1]
            station_utm.append(stat)

            
        
    minx = min (station["x"] for station in station_utm)
    miny = min (station["y"] for station in station_utm)
    maxx = max (station["x"] for station in station_utm)
    maxy = max (station["y"] for station in station_utm)

    min_lat = min(station["lat"] for station in station_utm)
    max_lat = max(station["lat"] for station in station_utm)
    min_lon = min(station["long"] for station in station_utm)
    max_lon = max(station["long"] for station in station_utm)



    minpos = utm.from_latlon(min_lat, min_lon)
    maxpos = utm.from_latlon(max_lat, max_lon)
    
    
    sizex = maxx - minx
    sizey = maxy - miny
    xmin = minx
    ymin = miny
    ymax = maxy
    
    # print (minpos, maxpos)
    # print ("width ", sizex)  
    # print ("height", sizey)  
    # print ("xmin ymin", xmin, ymin)
    # print (width / sizex, height / sizey)
    ratio = min (width / sizex, height / sizey)
    print ("ratio", ratio)

    elements: list[svg.Element] = []
        
        
    for line in transport_2d_data:
        station_utm = []
        path : list[svg.element] = []
        print("tracing line:", line["name"], line)
        for station in line["stations"]:
            stat = station.copy()
            pos = proj.transform_point(station["long"], station["lat"], data_proj)
            #pos = utm.from_latlon(station["lat"], station["long"])
            stat["x"] = pos[0]
            stat["y"] = pos[1]
            station_utm.append(stat)    
            

        position = []
        for station in station_utm:
            #pos = utm.from_latlon(station["lat"], station["long"])
            x = round((station['x'] - xmin) * ratio, 2)
            y = round((station['y'] - ymin) * ratio, 2)
            print (x,y)
            position.append( (x,y) )

        if len(position) > 0:
            path.append (svg.M(position[0][0],position[0][1]))

        for pos in position[1:]:    
            #print (pos[0],pos[1])    
            path.append (svg.L(pos[0],pos[1]))
        
        elements.append(svg.Path(
                    stroke="#ff0000",
                    stroke_width=4,
                    stroke_linecap="round",
                    fill="none",
                    d=path,
                ))
        
    fig = svg.SVG(
                viewBox=svg.ViewBoxSpec(0, 0, width, height),
                width=svg.mm(width),
                height=svg.mm(height),
                elements=elements
                )
    with open('test.svg', 'w') as f:
        f.write(str(fig))
    return fig