

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