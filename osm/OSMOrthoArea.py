

class OrthoArea:
    def __init__ (self):
        # Initialize the minimum and maximum x and y coordinates
        self.minx = 100000000
        self.miny = 100000000
        self.maxx = -100000000
        self.maxy = -100000000
        self.width = 0
        self.height = 0
        self.marginx = 50
        self.marginy = 50
        self.ratio = 1
        # Initialize the minimum and maximum latitude and longitude
        self.min_lat = 100000000
        self.max_lat = -100000000
        self.min_lon = 100000000
        
        self.max_lon = -100000000


    def AddPoint (self, x, y):
        # Update the minimum and maximum x and y coordinates
        self.minx = min ([self.minx, x])
        self.miny = min ([self.miny, y])
        self.maxx = max ([self.maxx, x])
        self.maxy = max ([self.maxy, y])

    def AddLatLon (self, lat, lon):
        # Update the minimum and maximum latitude and longitude
        self.min_lat = min([self.min_lat, lat])
        self.max_lat = max([self.max_lat, lat])
        self.min_lon = min([self.min_lon, lon])
        self.max_lon = max([self.max_lon, lon])