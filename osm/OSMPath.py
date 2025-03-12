import shapely
import svg
from . import OSMsvgFile
import math

class OSMPath:

    def __init__(self, points = []):
        # Initialize the OSMPath object with a list of points
        self.points = points

        

    def setPoints (self, points):
        # Set the points of the OSMPath object
        self.points = points

    def addPoint (self, point):
        """
        Add a point to the OSMPath object.

        Args:
            point (tuple): The point to be added, represented as a tuple of coordinates (latitude, longitude).
        """
        self.points.append (point)

    def getPoints (self):
        """
        Return the points of the OSMPath object.

        Returns:
            list: A list of points representing the OSMPath.
        """
        return self.points

    def getLength (self):
        """
        Return the length of the OSMPath object.

        Returns:
            int: The length of the OSMPath object, which is the number of points in the path.
        """
        return len (self.points)

    def getPoint (self, index):
        """
        Retrieves a point from the list of points.

        Args:
            index (int): The index of the point to retrieve.

        Returns:
            Point: The point at the specified index.
        """
        
        return self.points[index]
    
    def DrawSVGPath (self, svgfile, points, strokecolor, stroke_width, fillcolor):
        """
        Draw an SVG path with the given points, stroke color, stroke width, and fill color.

        Parameters:
        svgfile (svg.SVG): The SVG file to which the path will be added.
        points (list[tuple[float, float]]): A list of points that define the path. Each point is a tuple of (x, y) coordinates.
        strokecolor (str): Stroke color.
        stroke_width (float): The width of the stroke.
        fillcolor (str): fill color.

        Returns:
        None
        """
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

    def DrawPath (self, fsvg, color, width, fillcolor, aspolygon=False):
        """
        Draw the OSMPath object as an SVG path.

        Parameters:
        fsvg (file-like object): The file-like object to write the SVG path to.
        color (str): The color of the path.
        width (float): The width of the path.
        fillcolor (str): The fill color of the path.
        aspolygon (bool, optional): If True, draw the path as a polygon. Defaults to False.
        """
        # Draw the OSMPath object as an SVG path
        if aspolygon:
            # If the OSMPath object is to be drawn as a polygon, create a LineString from the points and buffer it
            line = shapely.LineString (self.points)
            offseted = shapely.buffer (line, width / 2)
            coords = shapely.get_coordinates(offseted)

            # Draw the buffered path
            self.DrawSVGPath (fsvg, coords, color, 0.1, fillcolor)
        else:
            
            # If the OSMPath object is not to be drawn as a polygon, draw the path as is
            self.DrawSVGPath (fsvg, self.points, color, width, fillcolor)
