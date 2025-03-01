import sys
import os





if __name__ == '__main__':
    

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print (SCRIPT_DIR)
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    
    from osm import OSMsvgFile
    from osm import OSMSymbol
    

    fsvg = OSMsvgFile.OSMsvgFile ()
    fsvg.open (widthmm=500, heightmm=500)
    
    symbol = OSMSymbol.OSMSymbol ()
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Circle, 100,100,100, "none", "red")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Square, 200,100,100, "none", "yellow")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Triangle, 100,200,100, "none", "green")
    
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Star, 200,200,100, "none", "blue")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Cross, 300,100,100, "none", "blue")

    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Circle, 100,100,80, "black", "red")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Square, 200,100,80, "black", "yellow")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Triangle, 100,200,80, "black", "green")
    
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Star, 200,200,80, "black", "blue")
    symbol.DrawSymbol (fsvg, OSMSymbol.OSMSymbolType.Cross, 300,100,80, "black", "blue")

    fsvg.close ()
    fsvg.writeToFile ("testsymbol.svg")
