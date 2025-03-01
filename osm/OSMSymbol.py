import shapely
import svg
from enum import Enum
from . import OSMsvgFile
import math

class OSMSymbolType(Enum):
    Circle = 0
    Star = 1
    Square = 2
    Triangle = 3
    Cross = 4

class OSMSymbol:
    def __init__(self):
        pass

    def DrawSymbol (self, svgfile, symbol, x, y, size, fillcolor, strokecolor):
        print ("Drawsymbol", symbol)
        match (symbol):
            case OSMSymbolType.Circle:
                print ("draw circle")
                svgfile.addsvg (svg.Circle(cx=x, cy=y, r=size/2, fill=fillcolor, stroke=strokecolor, stroke_width=1))
            case OSMSymbolType.Star:
                
                points = []
                angle_step = math.pi / 5  # 

                for i in range(11):  # 5 sommets + 5 branches
                    r = size/2 if i % 2 == 0 else size / 4  # Rayon alterné pour les branches
                    angle = i * angle_step 
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
               
                    points.append( (px, py) )
                
                path : list[svg.Element] = []
                path.append (svg.M (points[0][0], points[0][1]))
                for p in points[1:]:
                    path.append (svg.L (p[0], p[1]))
                
                svgfile.addsvg(svg.Path(
                                stroke=strokecolor,
                                stroke_width=1,
                                stroke_linecap="round",
                                fill=fillcolor,
                                d=path,
                            ))
            case OSMSymbolType.Square:
                svgfile.addsvg (svg.Rect(x=x-size/2, y=y-size/2, width=size, height=size, fill=fillcolor, stroke=strokecolor, stroke_width=1))

            case OSMSymbolType.Triangle:    
                svgfile.addsvg (svg.Polygon(points=[(x, y-size/2), (x+size/2, y+size/2), (x-size/2, y+size/2)], fill=fillcolor, stroke=strokecolor, stroke_width=1))

            case OSMSymbolType.Cross:   
                points = [
                        (x-size/4, y-size/2), (x+size/4, y-size/2), 
                        (x+size/4, y-size/4), (x+size/4, y-size/2), 
                        (x+size/4, y-size/4), (x+size/2, y-size/4), 
                        (x+size/2, y+size/4), (x+size/4, y+size/4), 
                        (x+size/4, y+size/2), (x-size/4, y+size/2), 
                        (x-size/4, y+size/4), (x-size/2, y+size/4), 
                        (x-size/2, y-size/4), (x-size/4, y-size/4), 
                        (x-size/4, y-size/2) 
                        ]
                path : list[svg.Element] = []
                path.append (svg.M (points[0][0], points[0][1]))
                for p in points[1:]:
                    path.append (svg.L (p[0], p[1]))
                
                svgfile.addsvg(svg.Path(
                                stroke=strokecolor,
                                stroke_width=1,
                                stroke_linecap="round",
                                fill=fillcolor,
                                d=path,
                            ))
