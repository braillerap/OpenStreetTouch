

class OSMTransitInfo ():
    def __init__ (self):
        self.stations = {}

    def SetStationInfos (self, Stationdic):
        self.stations = Stationdic

    def IsStationTransit (self, station):
        if (station in self.stations):
            return (self.stations[station] > 2)
        return False