import shapely
import svg
from . import OSMsvgFile
import math

class OSMPath:

    def __init__(self, points = []):
        self.points = points

        

    def setPoints (self, points):
        self.points = points

    def addPoint (self, point):
        self.points.append (point)

    def getPoints (self):
        return self.points

    def getLength (self):
        return len (self.points)

    def getPoint (self, index):
        return self.points[index]
    
    def DrawSVGPath (self, svgfile, points, strokecolor, stroke_width, fillcolor):
        path : list[svg.Element] = []
        if len (points) > 1:
            start = points[0]
            path.append(svg.M(float(start[0]), float(start[1])))
            for point in points[1:]:
                path.append(svg.L(float(point[0]), float(point[1])))

            svgfile.addsvg(
                        svg.Path(
                            stroke=strokecolor,
                            stroke_width=stroke_width,
                            stroke_linecap="round",
                            fill=fillcolor,
                            d=path,
                    ))

    def DrawPath (self, fsvg, color, width, aspolygon=False):
        if aspolygon:
            line = shapely.LineString (self.points)
            offseted = shapely.buffer (line, width / 2)
            coords = shapely.get_coordinates(offseted)

            self.DrawSVGPath (fsvg, coords, color, 0.1, color)
        else:
            self.DrawSVGPath (fsvg, self.points, color, width, "none")
            