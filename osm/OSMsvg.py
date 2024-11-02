import svg
import utm
import cartopy.crs as ccrs

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
            #print (x,y)
            position.append( (x,y) )

        if len(position) > 0:
            path.append (svg.M(position[0][0],position[0][1]))

        for pos in position[1:]:    
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