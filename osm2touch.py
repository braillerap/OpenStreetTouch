import os
import platform
import threading
import webview
import json
import platform
import sys
import time
from pathlib import Path
from osm import OSMprocess
from osm import OSMprocessStreet
from osm import OSMutils


rpi = False
COM_TIMEOUT =   5  #Communication timeout with device controller (Marlin)

if getattr(sys, "frozen", False):
    try:  # pyi_splash only available while running in pyinstaller
        import pyi_splash
    except ImportError:
        pass

app_options = {
    
    "lang": "en",
    
}



class KnownOS:
    Windows = 0
    Linux = 1
    RPI = 2
    Unknown = 3



filename = ""
root = None

detected_os = KnownOS.Unknown

def get_parameter_fname ():
    paramfname = "osm2touch_parameters.json"
    if detected_os == KnownOS.Linux:
        home = Path.home ()
        dir = Path.joinpath(home, ".osm2touch/")
        print (home, dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = Path.joinpath(dir, paramfname)
        print (fpath)
        return fpath

    else:
        return paramfname
        
def load_parameters():
    try:
        fpath = get_parameter_fname()

        with open(fpath, "r", encoding="utf-8") as inf:
            data = json.load(inf)
            for k, v in data.items():
                if k in app_options:
                    app_options[k] = v

    except Exception as e:
        print(e)
    print(app_options)


class Api:
    def __init__(self):
        self.osmt = OSMprocess.Osmprocess()
        self.osms = OSMprocessStreet.OSMprocessStreet()
        self._window = None

    def fullscreen(self):
        """toggle main window fullscreen"""
        webview.windows[0].toggle_fullscreen()

       

    def set_window(self, window):
        self._window = window

    def quit(self):
        print ("quit request")
        self._window.destroy()
    
    def gcode_get_parameters(self):
        """Get parameters value"""
        js = json.dumps(app_options)
        print ("backend get parameters: ", js)
        return js

    def gcode_set_parameters(self, opt):
        """Set parameters value"""
        print("parameters", opt, type(opt))
        try:
            for k, v in opt.items():
                if k in app_options:
                    app_options[k] = v

        except Exception as e:
            print(e)
        self.save_parameters()

    def confirm_dialog (self, title, message):
        return window.create_confirmation_dialog(title, message)
    
    def save_parameters(self):
        """Save parameters in local json file"""
        try:
            #print("data", app_options)
            #print("json", json.dumps(app_options))
            fpath = get_parameter_fname()
            with open(fpath, "w", encoding="utf-8") as of:
                json.dump(app_options, of)

        except Exception as e:
            print(e)

    
    def saveas_svg_aspngfile (self, svgdata, dialogtitle, filterstring):
        pass
        # global filename

        # fname = window.create_file_dialog(
        #     webview.SAVE_DIALOG,
        #     allow_multiple=False,
        #     file_types=(filterstring[0] + " (*.svg)", filterstring[1] + " (*.*)"),
        # )
      
        # if fname:
        #     if detected_os == KnownOS.Windows:
        #         filename = fname
        #     else:
        #         filename = fname[0]
        # else:
        #     return
        
        # svg2png(bytestring=svgdata,write_to=filename)

    def saveas_svgfile(self, data, dialogtitle, filterstring):
        global filename

        fname = window.create_file_dialog(
            webview.SAVE_DIALOG,
            allow_multiple=False,
            file_types=(filterstring[0] + " (*.svg)", filterstring[1] + " (*.*)"),
        )
      
        if fname:
            if detected_os == KnownOS.Windows:
                filename = fname
            else:
                filename = fname[0]
        else:
            return
        
        with open(filename, "w", encoding="utf8") as inf:
            inf.writelines(data)
    def saveas_file(self, data, dialogtitle, filterstring):
        global filename

        fname = window.create_file_dialog(
            webview.SAVE_DIALOG,
            allow_multiple=False,
            file_types=(filterstring[0] + " (*.txt)", filterstring[1] + " (*.*)"),
        )
      
        if fname:
            if detected_os == KnownOS.Windows:
                filename = fname
            else:
                filename = fname[0]
        else:
            return
        
        with open(filename, "w", encoding="utf8") as inf:
            inf.writelines(data)

    def save_file(self, data, dialogtitle, filterstring):
        global filename
        if filename == "":
            self.saveas_file (data, dialogtitle, filterstring)
            return

        with open(filename, "w", encoding="utf8") as inf:
            inf.writelines(data)

    def download_file(self, data, dialogtitle, filterstring, filter=["(*.txt)", "(*.*)"]):
        
        if len(filterstring) < 2 or len(filter) < 2:
            print("incorrect file filter")
            return 

        fname = window.create_file_dialog(
            webview.SAVE_DIALOG,
            allow_multiple=False,
            file_types=(filterstring[0] + " " + filter[0], filterstring[1] + " " +filter[1]),
        )
      
        if fname:
            if detected_os == KnownOS.Windows:
                ftowrite = fname
            else:
                ftowrite = fname[0]
        else:
            return
        
        with open(ftowrite, "w", encoding="utf8") as inf:
            inf.writelines(data)

    def read_file (self, path):
        js = {"data": "", "error": ""}
        with open(path, "rt", encoding="utf8") as inf:
            js["data"] = inf.read()
            js["fname"] = os.path.basename(path)
            

        return json.dumps(js)
    
    def import_file(self, dialogtitle, filterstring, filter=["(*.brp)", "(*.*)"]):
        
        js = {"data": "", "error": ""}

        # check file filter
        if len(filterstring) < 2 or len(filter) < 2:
            js["error"] = "incorrect file filter"
            return json.dumps(js)

        # open common dialog
        listfiles = window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=(filterstring[0] + " " + filter[0], filterstring[1] + " " +filter[1]),
        )
        if not listfiles:
            return json.dumps(js)
        if len(listfiles) != 1:
            return json.dumps(js)
        fname = listfiles[0]
        
        if fname == "" or fname == None:
            return json.dumps(js)

        with open(fname, "rt", encoding="utf8") as inf:
            js["data"] = inf.read()
            js["fname"] = os.path.basename(fname)
            

        return json.dumps(js)
    
    def load_file(self, dialogtitle, filterstring, filter=["(*.brp)", "(*.*)"]):
        global filename
        js = {"data": "", "error": ""}

        # check file filter
        if len(filterstring) < 2 or len(filter) < 2:
            js["error"] = "incorrect file filter"
            return json.dumps(js)

        # open common dialog
        listfiles = window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=(filterstring[0] + " " + filter[0], filterstring[1] + " " +filter[1]),
        )

        if not listfiles:
            return json.dumps(js)
                
        if len(listfiles) != 1:
            return json.dumps(js)
        
        if listfiles[0]:
            fname = listfiles[0]
        else:
            return json.dumps(js)
        
        with open(fname, "rt", encoding="utf8") as inf:
            js["data"] = inf.read()
            filename = fname

        return json.dumps(js)
    
    def GetISO639_country_code (self):
        list = OSMutils.omsutils_get_iso639_code ()
        print(list)
        return list
    
    def ReadTransportData (self, city, transport_type, iso639_city_code, place_id):
        ret = self.osmt.ReadTransportData (city, transport_type, iso639_city_code, place_id)
        print ("ReadTransportData", ret)
        return ret
    

    def GetTransportLines (self):
        #ret = self.osmt.GetTransportLineList ()
        ret = self.osmt.GetTransportDataLineList ()
        
        print ("GetTransportLineList", ret)
        return ret

    def GetTransportDataSvg (self, linelist, drawstation, linestrategy, polygon):
        print ("GetTransportSVG", linelist, drawstation, int(linestrategy), type(linestrategy))

        svg = self.osmt.GetTransportDataSvg (linelist, drawstation, int(linestrategy), polygon)
        print ("GetTransportSVG svg size", len(svg))
        return svg
    
    def GetTransportData (self, linelist, drawstation, linestrategy, polygon):
        svg = self.GetTransportDataSvg (linelist, drawstation, linestrategy, polygon)
        liststation = self.osmt.GetTransportDataStations (linelist)

        return json.dumps({"svg": svg, "stations": liststation})
    
    def GetTransportSVGbase64 (self):
        svg = self.osmt.get_svg ()
        return svg

    

    def ReadStreetMapData (self, latitude, longitude, radius, building, footpath, polygon):
        street_data = self.osms.ReadStreetMapData (latitude, longitude, radius)
        print ("building", building, "footpath", footpath, "polygon", polygon)
        svg = self.osms.GetStreetMapSVG (street_data, latitude, longitude, building, footpath, polygon)
        print ("ReadStreetMapData svg size", len(svg))
        return svg
    
def get_entrypoint():
    def exists(path):
        print(os.path.join(os.path.dirname(__file__), path))
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

   
    if exists("./build/index.html"):  # unfrozen development
        return "./build/index.html"

    raise Exception("No index.html found")




def delete_splash(window):
    print ("delete splash **************************************************")
    
    
    try:
        if (platform.machine () == 'aarch64'):
            time.sleep(10)
            print ("#################################  resize the window")
            window.resize (512,512)
            window.maximize()
    except:
        pass
        
    try:
        if getattr(sys, "frozen", True):
            pyi_splash.close()
    except:
        pass


    

    
    # print ("started", time())


entry = get_entrypoint()

if __name__ == "__main__":
    app = "Osm2Touch"
    api = Api()
    debugihm = True

    #print(sys.argv)
    dir, script = os.path.splitext(sys.argv[0])
    if len(sys.argv) > 1 and script == ".py":
        if sys.argv[1] == "--debug":
            debugihm = True

    # display html start file
    print("start html=", entry)
    
    # load parameteres
    load_parameters()

    # start gui
    if platform.machine() == 'aarch64':
        detected_os = KnownOS.RPI
    if platform.system() == "Windows":
        detected_os = KnownOS.Windows
    elif platform.system() == "Linux":
        detected_os = KnownOS.Linux

    if detected_os == KnownOS.RPI:    
        window = webview.create_window(
            app, entry, js_api=api, focus=True,
        )
    else:
        window = webview.create_window(
            app, entry, js_api=api, focus=True, maximized=True,
        )
    
    api.set_window (window)

    if detected_os == KnownOS.Windows:
        print ("starting Windows GUI")
        webview.start(delete_splash, window, http_server=False, debug=debugihm)
    elif (detected_os == KnownOS.Linux):
        #set QT_QPA_PLATFORM on UBUNTU
        if getattr(sys, 'frozen', False):
            
            if ('QT_QPA_PLATFORM' in os.environ):
                print ("QT_QPA_PLATFORM=", os.environ['QT_QPA_PLATFORM'])
                print ("starting Linux GUI QT with configured QT_QPA_PLATFORM")
                webview.start(delete_splash, gui="qt", http_server=False, debug=False)
            else:
                print ("QT_QPA_PLATFORM=<empty>")
                print ("try to resolve with XDG_SESSION_TYPE")
                plugin = 'xcb'

                if ('XDG_SESSION_TYPE' in os.environ):             
                    if (os.environ['XDG_SESSION_TYPE'] == 'wayland'):
                        plugin = 'wayland'
                    
                # try wayland and xcb to start QT
                print ("setting QT_QPA_PLATFORM to :", plugin)
                os.environ['QT_QPA_PLATFORM'] = plugin
                
                                
                webview.start(delete_splash, window, gui="qt", http_server=False, debug=False)
                                
                
        else :
            print ("starting  GUI GTK dev environment, debug don't work in qt")
            webview.start(delete_splash, window, gui="gtk", http_server=False, debug=debugihm)
