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
    def DrawSymbol (self, svgfile, symbol, x, y, size, fillcolor, strokecolor):
        """
        Draws the specified symbol at a given position with a specified size and color.

        Parameters:
        svgfile (svg.SVGFile): The SVG file to which the symbol will be added.
        symbol (OSMSymbolType): The type of symbol to draw.
        x (float): The x-coordinate of the symbol's center.
        y (float): The y-coordinate of the symbol's center.
        size (float): The size of the symbol.
        fillcolor (str): The fill color of the symbol.
        strokecolor (str): The stroke color of the symbol.
        """
        
        match (symbol):
            case OSMSymbolType.Circle:
                """
                Draws a circle symbol.
                """
                svgfile.addsvg (svg.Circle(cx=x, cy=y, r=size/2, fill=fillcolor, stroke=strokecolor, stroke_width=1))
            case OSMSymbolType.Star:
                """
                Draws a star symbol.
                """
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
                """
                Draws a square symbol.
                """
                svgfile.addsvg (svg.Rect(x=x-size/2, y=y-size/2, width=size, height=size, fill=fillcolor, stroke=strokecolor, stroke_width=1))

            case OSMSymbolType.Triangle:    
                """
                Draws a triangle symbol.
                """
                svgfile.addsvg (svg.Polygon(points=[(x, y-size/2), (x+size/2, y+size/2), (x-size/2, y+size/2)], fill=fillcolor, stroke=strokecolor, stroke_width=1))

            case OSMSymbolType.Cross:   
                """
                Draws a cross symbol.
                """
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
