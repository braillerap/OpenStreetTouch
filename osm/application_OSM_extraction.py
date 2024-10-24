
"""
   Extraction from open street map of transportation network lines 

   this code is released under license : open source CeCILL : http://www.cecill.info/ 

   CC-BY-SA

"""

# modules 
import datetime
import matplotlib.pyplot as plt
import os 
import pandas as pd
import re
import requests
import sys 
import time
# module lecture fichier de configuration
import configparser 
import ast 

from io import BytesIO
import base64

#~DATA 
__version__ = "1.0 beta"
__date__ = "02/08/2024"
__status__ = "ok"
__authors__ = "François, Stéphane et Gabriel" 
__organization__ = "My Human Kit - Rennes, France" 
__licence__ = "CeCILL v2.1 / CC by SA"

#-----------------------------------
#
# FUNCTIONS 
#
#-----------------------------------

# function to read configuration file 
def read_configuration_file(input_config_file):
    """Read configuration file 
    
    input : 
    -------
    
        input_config_file : configuration file name (str) 
        
    returns:
    --------

        dictionnary conaining all sections, keys and values 
    """
    # create ConfigParser object 
    config = configparser.ConfigParser()

    # read config file (.ini) 
    # loadin config ini in UTF-8 encoding 
    with open(input_config_file, encoding='utf-8') as f_ini:
        config.read_file(f_ini)

    # convert config data to dictionnary 
    config_dict = {section: dict(config.items(section)) for section in config.sections()} 
    
    return config_dict 
    
# function for overpas request on Open Street Map database 
def overpass_request(place_name, transportation_type = "subway"): 
    """Fonction : overpass request data 
    
    Parameters :
    ------------
        place_name : str 
            name of the area : example "Rennes" 
            
        transportation_type : str 
            type of network : for example "subway" use to extract relation["route"="{transportation_type}"] 
    Return :
    --------
        df_raw_data : pandas dataframe including returned data 
        
        status : status returned by request command 
        
    """
    
    # URL 
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # ajout d'une majuscule sur la première lettre de place_name 
    place_name = place_name.capitalize()
    
    # Modifier l'overpass_query pour récupérer les données des arrêts de métro.
    overpass_query = f"""
    [out:json][timeout:30];
    /* recherche des données avec .searcharea */ 
    area["name"="{place_name}"]->.searcharea;
    (
      relation["type"="route"]["route"="{transportation_type}"](area.searcharea);  
    );
    out ;
    >;
    out body qt ;
    """

    # print("Requête pour la ville {}".format(place_name))
    
    # response = requests.get(overpass_url, params={'data': overpass_query})
    try:
        response = requests.post(overpass_url, data={'data': overpass_query})
    except Exception as e:
        print("Request error")
        print(e) 
        return {}
        
    # status = response.raise_for_status()  # Vérifie si la requête a échoué
    # print("status : ", status) 
    # data = response.json()
        
    # Vérifier le statut de la réponse
    if response.status_code == 200:
        # Parser la réponse JSON
        data = response.json()
        # print(data)
    else:
        data = {}
        print(f"Erreur: {response.status_code}")
        print(response.text)

    return data
    # fin fonction interrogation 

# Fonction line_extraction 
def line_extraction(data):
    """lin extraction fonction 
    
    parameter
    --------
        data : data dictionnary (result of overpass query preformed on Open street Map 
        
        Returns 
        -------
            metro_line_info : list  
        """ 
    
    metro_lines_info = list() 
    
    if not data['elements']:
        print("Aucune donnée récupérée pour la ville {}".format(place_name))
    else:
        # Parcourir les éléments de données pour obtenir les informations des lignes de métro dans le dictionnaire data
        # element.keys()
        #  dict_keys(['type', 'id', 'nodes', 'tags']) 
        for element in data['elements']:
            # print("Élément : ", element)
            # Extraction des relations pour extraire les lignes de métro a et b

            # test : pour trouver une relation qui correspond à une ligne de métro 
            # 1 : la varialbe element est de type dictionnaire 
            # 2 : et element['type'] == "relation" 
            if isinstance(element, dict) and element['type'] == 'relation':
                print("\nLigne : ", element['type'])
                # metro_line = element['tags'].get('ref', 'Unnamed')
                element_type = element['tags']["type"] 
                transport_type = element['tags']["route"]
                line_name = element['tags']["name"]
                from_station = element['tags']["from"]
                to_station = element['tags']["to"]
                
                print("nom de la liigne : ", line_name) 
                line_label = element['tags']["ref"]
                # type de réseau de transport 
                # element['tags']["type"] = "route" 
                # element['tags']["route"] = "subway" 
                print("Type : ", element_type) 
                print("Moyen de transport : ", transport_type) 
                print("-----------------")
                
                # Extraction du nom de la ligne => OK
                
                # extraction des stations de métro de la ligne 
                # initialisation de la liste des stations de la ligne considérée
                metro_stops = []
                
                # initialisation du dictionnaire qui décrit une station 
                metro_station = {}
                
                # boucle sur les membres de la relation 
                # member.keys()
                #    dict_keys(['type', 'ref', 'role'])
                # print("Boucle sur les membres de la relation :") 
                for member in element['members']:
                    # print("Member : ")
                    # print("=> type : ", member['type'])
                    # print("=> Ref : ", member['ref'])
                    # print("=> Role : ", member['role'])
                    # test de member 
                    # 1 : member est de type dictionnaire
                    # 2 : le role est égal à "stop" 
                    # MODIFICATION FLB 
                    # 2 : le type = node 
                    if isinstance(member, dict) and member['type'] == 'node':
                        # print(">>> Membre avec rôle 'stop'")
                        node_id = member['ref']
                        # print(">>> Node Id : ", node_id)
                        # recherche de ce noeud dans la lisste des noeuds qui composent la relation  
                        # --------------------------------------------------------------------------
                        # le nom de la station est dans : node_element["tags"]["name"]
                        # print(" boucle sur les noeuds ") 
                        # print("----------------------")
                        # on parcours la liste des noeuds dans data["elements"] pour identifier les noeuds qui apparatienent à la relation de la ligne 
                        for node_element in data['elements']:
                            # print("node_element ; ", node_element)
                            # test : ce node est-il membre de la relation qui représente la ligne ?
                            # 1 : node_element doit être de type dictionnaire 
                            # 2 : type = "node" et type = "node_id" 
                            #
                            # MODIFICATION DU CODE :
                            # NOTE FLB : filtrage des nodes avec : "public_transport"="stop_position" + "subway" = "yes"
                            # SUPRESSION du type = node 
                            # if isinstance(node_element, dict) and node_element['type'] == 'node' and node_element['id'] == node_id:
                            if isinstance(node_element, dict) and node_element['id'] == node_id:
                                #  node_element.keys()
                                #    dict_keys(['type', 'id', 'lat', 'lon', 'tags'])
                                # print("node_element ; ")
                                # print("=> type : ", node_element['type'])
                                # print("=> id : ", node_element['id'])
                                # print("=> latitude : ", node_element['lat'])
                                # print("=> longitude : ", node_element['lon'])
                                # print("=> public_transport : ", node_element['tags']["public_transport"])
                                # print("=> subway : ", node_element['tags']["subway"])
                                # print("Node name : ", node_element['tags']["name"])
                                # test sur les caractéristiques du neode 
                                # pour déterminer si la station doit être retenue 
                                # 1 : la clé "tags" doit exister 
                                # 2 : et la clé "name" doit exister dans le dict node_element["tags"] 
                                if 'tags' in node_element and 'name' in node_element['tags']:
                                    metro_station["line_label"] = line_label
                                    metro_station["name"] = node_element['tags']['name']
                                    # metro_station["public_transport"] = node_element['tags']["public_transport"]
                                    metro_station["lon"] =  node_element['lon']
                                    metro_station["lat"] =  node_element['lat']
                                    # clé railway peut prendre les valeurs : subway, rail ou tram 
                                    if metro_station["name"] == "Gares": 
                                        print("gare ") 
                                        gare = node_element
                                        print("")
                                        print(node_element) 
                                        print("") 
                                         
                                    # print("ajouter : ", metro_station) 
                                    # ajout du nom de la station à la liste de la ligne 
                                    # à partir du dictionnaire, mais penser à ajouter la méthode copy pour éviter les duplications !
                                    metro_stops.append(metro_station.copy())
                                    
                                    # print("mise à jour liste des stations de la ligne : ")
                                    # affichage des éléments de la liste des stations de la ligne 
                                    # on utilise l'opérateur de décompression (ou opérateur "splat") en Python. 
                                    # Il est utilisé pour décompresser (ou "dépaqueter") une collection d'éléments 
                                    # (comme une liste, un tuple, ou dans ce cas, une expression génératrice) en arguments individuels pour une fonction
                                    # print(*(f"{s}\n" for s in metro_stops), sep='')
                                else:
                                    print("Aucun nom de station trouvé pour le noeud : ", node_id)
                                # fin if 'tags' in node_element and 'name' in node_element['tags']
                            # fin if isinstance(node_element, dict) and node_element['id'] == node_id    
                        # fin boucle for node_element in data['elements']:
                    # fin if isinstance(member, dict) and member['type'] == 'node':
                # fin de boucle for member in element['members']:
                
                # Apres avoir identifié les nodes qui correspondeut aux stations de la ligne 
                # on identifie la tête et la fin de la ligne 
                # on structure les données souss forme de dataframe 
                # print("\nRécapitulatif de la ligne : ") 
                # print(f"Ligne : {line_label}.")
                # print(f"From : {from_station}")
                # print(f"To : {to_station}")
                
                # print("nombre de stations : ", len(metro_stops)) 
                # print("liste des stations identifiées :")
                # affichage des éléments de la liste de la ligne 
                # print(*(f"{s}\n" for s in metro_stops), sep='')
                
                # structuration d'une liste incluant l'ensemble des infos de la ligne 
                for i, stop_name in enumerate(metro_stops):
                    metro_lines_info.append({
                        'line_label': line_label,
                        "line_name" : line_name,
                        'from_station': from_station,
                        'to_station': to_station,
                        'station_order': i + 1,
                        'station_name': metro_stops[i]["name"],
                        "longitude [deg]" : metro_stops[i]["lon"],
                        "latitude [deg]" : metro_stops[i]["lat"]
                        })
                    # print("Ajout de la ligne de métro : ", line_name)
            # fin if if isinstance(element, dict) and element['type'] == 'relation':     
        # fin boucle for element in data['elements']:
        # Fin de boucle sur les lignes
    # fin if not data['elements']:
    return metro_lines_info
    # fin de fonction 

# fonction plot_network (matplotlib) 
def plot_network(df_line_info, fig_width_inches, fig_height_inches, background_color, dpi):
    """Function to plot transportation network 
    
    Parameters :
    ------------
        df_line_info : dataframe describing station list and positions 
            columns are : 
            Index(['line_label', 'line_name', 'from_station', 'to_station',
                   'station_order', 'station_name', 'longitude [deg]', 'latitude [deg]',
                   'crossing', 'crossing_lines'],
                   dtype='object')
        
        fig_width_inches : 
        
        fig_height_inches :
        
        background_color :
        
        dpi :
        
    output :         
    --------    
        fig : figure object produced with matplotlib 
    """
    
    # Défine lines and markers styles 
    line_styles = ['-', '--', '-.', ':']
    markers_styles = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '+', 'x']
    marker_size = 10 
    crossing_marker_size = 12 
    crossing_marker = '*'
    crossing_color = "black" 
    color_list = ["green", "blue", "cyan", "magenta", "yellow", "orange", "gray", "olive", "purple",  "pink", "brown", "lime"]
    
    # print("fig_width_inches : ", fig_width_inches) 
    # print("fig_height_inches : ", fig_height_inches) 
    # print("background_color : ", background_color ) 
    # print("dpi : ", dpi)

    # filtering df_line_info to get only one direction for each metro line 
    df_line_list = df_line_info.groupby([ 'line_label', 'line_name']).size().reset_index(name='counts')
    df_one_line_every_two = df_line_list.iloc[::2] 
    
    # create figure 
    fig = plt.figure(figsize=(fig_width_inches, fig_height_inches), facecolor = background_color, dpi=dpi)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    # add axes 
    ax = fig.add_subplot(111)

    # add lines  for only one direction on the same line 
    for idx, line in enumerate(df_one_line_every_two["line_label"].replace(":"," : ")):
        # print("add line : ", line)
        # line selection in df_line_info 
        filtered_df = df_line_info[df_line_info['line_label'] == line][['line_label', 'station_order', 'station_name', 'longitude [deg]', 'latitude [deg]', "crossing"]]
        
        # add line 
        ax.plot(filtered_df['longitude [deg]'], filtered_df['latitude [deg]'], 
                 label = line,
                 linestyle=line_styles[idx % len(line_styles)],
                 marker=None,
                 markersize=0,
                 linewidth = 2)    
        # plot station position with various markers versus crossing flag 
        for index, row in filtered_df.iterrows():
            marker = crossing_marker if row['crossing'] == 'yes' else markers_styles[idx % len(markers_styles)]
            station_color = crossing_color if row['crossing'] == 'yes' else color_list[idx % len(color_list)]
            station_marker_size = crossing_marker_size if row['crossing'] == 'yes' else marker_size
            # print("Marker : ", idx, marker)
            plt.plot(row['longitude [deg]'], row['latitude [deg]'], color = station_color,
                      marker = marker, markersize = station_marker_size, linewidth = 0)
        # end loop on station markers 
        
    # end of loop over lines 
    
    # plot configuration options 
    # plt.grid(False)
    
    #plt.show(block=False) 
    
    # end of loop for line tracing      """
    return fig 
    # end of function plot_network 

# function to copy figure in buffer to update html file 
def plot_to_buffer(fig):
    """function to send matplotlib figure to BytesIO buffer 
    
    Parameters :
    ------------
    
        figure : matplotlib figure object 
        
    Returns :
    ---------
    
        BytesIO buffer object 
    """

    buf = BytesIO()
    fig.savefig(buf, format='png')
    
    # Déplacement du curseur au début du buffer
    buf.seek(0)
    
    # convert buffer content to base64 
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
   
    # Fermer la figure pour libérer de la mémoire
    plt.close(fig)
        
    return image_base64
    # end of function plot to buffer 

# main function 
# -------------
def main(): 
    """main function :
            * creates overpass query and request data on Open Street Map 
            * Extracts network data (line names, types, and stations positions) 
            * plots lines network 
        """     
            
    metro_lines_info = list() 
    
    # répertoire de travail 
    print("Répertoire de travail : ", os.getcwd()) 

    # nom du fichier d'export du résultat brut de la requete overpass  
    output_file = 'test_export_elements_output.csv'

    # nom du fichier d'export des données relatives aux lignes extraites 
    output_file_line_info = "line_data_export.csv" 

    # read SCRIPT CONFIGURATION file 
    # ------------------------------

    # configuration file 
    input_config_file = "extraction_config.ini"

    print("Lecture du fichier de configuration : ", input_config_file) 
    config_data_dict = read_configuration_file(input_config_file) 

    # Access to configuration data (sections and keys) 
    # section_site = config['site name']
    # section_image_2D = config['image 2D']
    # section_couleurs_image = config['couleurs image']

    # read specific data 
    place_name = config_data_dict["site name"]["place_name"]
    # place_names_str = section_site.get('place_name')
    # place_names = ast.literal_eval(place_names_str)  # Évaluation de la chaîne comme une liste Python

    image_folder = config_data_dict["image 2D"]["image_folder"].strip('"')
    output_image_file_name = config_data_dict["image 2D"]['output_image_file_name'].strip('"')
    extension_file_format = config_data_dict["image 2D"]['extension_file_format'].strip('"')
    file_size = int(config_data_dict["image 2D"]['file_size'])
    dpi = int(config_data_dict["image 2D"]['dpi'])
    fig_width_mm = int(config_data_dict["image 2D"]['fig_width_mm'])
    fig_height_mm = int(config_data_dict["image 2D"]['fig_height_mm'])

    background_color = eval(config_data_dict["couleurs image"]['background_color']) # Évaluation de la chaîne comme une expression Python
    line_color = eval(config_data_dict["couleurs image"]['line_color'])
    station_color = eval(config_data_dict["couleurs image"]['station_color'])

    # show configuration data 
    print("Configuration data :") 
    print("----------------------------------")
    print("[site]")

    # on force la première lette du nom de la ville en majuscule pour les recherches dans OSM 
    print("place name:", place_name)

    print("\n[image 2D]")
    print("image_folder:", image_folder)
    print("Image file name : ", output_image_file_name) 
    print("extension_file_format:", extension_file_format)
    print("file_size:", file_size)
    print("dpi:", dpi)
    print("fig_width_mm:", fig_width_mm)
    print("fig_height_mm:", fig_height_mm)

    print("\n[couleurs image]")
    print("background_color:", background_color)
    print("line_color:", line_color)
    print("station_color:", station_color)

    # convert size in mm  
    un_pouce_mm = 25.4 # mm
    fig_width_inches = fig_width_mm / un_pouce_mm
    fig_height_inches = fig_height_mm / un_pouce_mm 

    # test image file folder exists and create it if necessary 
    if not os.path.exists(image_folder):
        # create sub-folder 
        os.makedirs(image_folder)
        print(f"sub-folder : {image_folder} created. ")
    else:
        print(f"sub-folder : {image_folder} already exists.")

    # create full path name with file extension      
    file_path = f"./{image_folder}/{output_image_file_name}.{extension_file_format}"

    # Définir la zone d'étude 
    # place_name = "Rennes"

    # type de transports
    # todo : ajouter dans le fichier de configuration .ini 
    transportation_type = "subway"  # => test ok 
    # transportation_type = "bus"  # => some bugs to be analysed...  
    # transportation_type = "tram" # sur Nantes => extraction de 10 relations dans les 2 sens 
    # transportation_type = "rail" # sur Rennes => aucun résultat 
    # transportation_type = "railway" # => ne fonctionne pas dans dans ce cas la relation n'a pas de clé "from" (et "to")  

    # create list to store line data 
    metro_lines_info = []
    
    print("")
    print("Sending overpass query.") 
    # overpass query for data extraction   
    try:
        data = overpass_request(place_name, transportation_type)
        # print(data)
    except Exception as e:
        print("Error") 
        print(e)
        sys.exit(1)

    # test of data content 
    if not data or 'elements' not in data or not data['elements'] or len(data['elements']) == 0:
        print("Data extraction ERROR !") 
        print("data is empty")
        print("or elements key is not define in data dict.") 
        print("or data[""elements""] is empty.") 
        print("Completd") 
        sys.exit() 
        
    # convert data dict  in dataframe 
    print("Convert data to dataframe format. ") 
    df_raw_data = pd.DataFrame(data["elements"])
       
    # Export DataFrame to CSV file. delimiter = ";" 
    print("Dataframe export into file : {}.".format(output_file)) 
    df_raw_data.to_csv(output_file, sep=';', index=False)

    # data analysis  
    # ------------- 
    # call function line_extraction 
    # return to list : metro_lines_info  
    metro_lines_info = line_extraction(data) 

    # convert extracted data list to pandas DataFrame 
    print("\`nCreate a pandas DataFrame...")
    df_line_info = pd.DataFrame(metro_lines_info)

    # identification des stations de corespondance 
    # Identifier les stations communes entre les lignes
    # Création d'une table croisée pour compter le nombre de lignes par station
    # on traite pour chaque ligne, les 2 sens de circulation. 
    # il faudra donc diviser par 2 les résultats pour ne considérer qu'une seule ligne 
    # avec un seul sens de circulation 
    df_station_counts = df_line_info.pivot_table(index="station_name", columns="line_label", aggfunc='size', fill_value=0)

    # Identification des stations communes
    # ATTENTION : la somme doit être supérieure à 2 
    # car le dataframe contient pour chaque ligne, les 2 sens de circulation 
    df_common_stations = df_station_counts[df_station_counts.sum(axis=1) > 2].index

    # Ajouter la colonne "crossing"
    df_line_info["crossing"] = df_line_info["station_name"].apply(lambda x: "yes" if x in df_common_stations else "no")

    # create dataframe containing station with crossing lines 
    df_crossing_lines_and_stations = df_line_info[df_line_info['crossing'] == 'yes'][['line_label', 'line_name', 'station_name', 'crossing']]
    
    # create dataframe containing for each crossing station, the list of lines 
    df_station_crossing_line_list = df_crossing_lines_and_stations.groupby('station_name')['line_label'].apply(lambda x: list(x.unique())).reset_index()
    
    # rename column "line_label" to "crossing_lines" 
    df_station_crossing_line_list.rename(columns={'line_label': 'crossing_lines'}, inplace=True)
    
    # Fusionner avec le DataFrame original
    # df_crossing_lines = df_crossing_lines.merge(df_line_list, on='station_name', how='left')
    df_line_info = df_line_info.merge(df_station_crossing_line_list, on='station_name', how='left')

    # print(metro_lines_info)
    # show DataFrame
    # print("\nDataFrame :")
    # print(df_line_info)

    # DataFrame export to CSV file 
    print("DataFrame export...")
    try:
        df_line_info.to_csv(output_file_line_info, sep = ";", index=False, encoding='utf-8')
        print(f"Data exportation into file : {output_file_line_info}")
    except Exception as e:
        print("Error : writing CSV file :", str(e))


    # available lines : df_line_info["line_name"].value_counts()
    print("\nLine list : ") 
    print("") 
    # print(df_line_info["line_name"].value_counts()) 

    # line extraction frome df_line_info  
    df_line_list = df_line_info.groupby([ 'line_label', 'line_name']).size().reset_index(name='counts')
    nombre_de_ligne = df_line_list.shape[0]

    print(f"\nExtraction of {nombre_de_ligne} lines.") 
    print("line list : ") 
    print(df_line_list)

    # est_paire = (nombre_de_ligne % 2) == 0

    # extraction of one_line_every_two   
    # 2 circulation ways extracted on the same line 
    # df_one_line_every_two = df_line_list.iloc[::2]
    # print("df_one_line_every_two") 
    # print(df_one_line_every_two) 
     
    # vérification de la présence de l'aller retour
    # df_line_list["line_label"].value_counts()

    # line liste and directions 
    #   df_line_info['line_name'].unique()

    # network plotting 
    # ----------------
        
    print("plot line network, 1 direction per line.") 
    fig = plot_network(df_line_info , fig_width_inches, fig_height_inches, background_color, dpi) 
    
    # ////// 
    # Save image
    print("Save image file : ", file_path )
    fig.savefig(file_path, dpi=400, bbox_inches="tight", format=extension_file_format)
    
    # return 
    # end main function 

# ////////////////////////////////////
# main function flask IHM 
# -------------
def main_flask_IHM(city_name = "None"): 
    """main function :
            * creates overpass query and request data on Open Street Map 
            * Extracts network data (line names, types, and stations positions) 
            * plots lines network 
        """     
            
    metro_lines_info = list() 
    
    # répertoire de travail 
    print("Répertoire de travail : ", os.getcwd()) 

    # nom du fichier d'export du résultat brut de la requete overpass  
    output_file = 'test_export_elements_output.csv'

    # nom du fichier d'export des données relatives aux lignes extraites 
    output_file_line_info = "line_data_export.csv" 

    # read SCRIPT CONFIGURATION file 
    # ------------------------------

    # configuration file 
    input_config_file = "extraction_config.ini"

    print("Lecture du fichier de configuration : ", input_config_file) 
    config_data_dict = read_configuration_file(input_config_file) 

    # Access to configuration data (sections and keys) 
    # section_site = config['site name']
    # section_image_2D = config['image 2D']
    # section_couleurs_image = config['couleurs image']

    # read specific data 
    place_name = city_name # from text label field of HTML form 
    # place_name = config_data_dict["site name"]["place_name"]
    # place_names_str = section_site.get('place_name')
    # place_names = ast.literal_eval(place_names_str)  # Évaluation de la chaîne comme une liste Python

    image_folder = config_data_dict["image 2D"]["image_folder"].strip('"')
    output_image_file_name = config_data_dict["image 2D"]['output_image_file_name'].strip('"')
    extension_file_format = config_data_dict["image 2D"]['extension_file_format'].strip('"')
    file_size = int(config_data_dict["image 2D"]['file_size'])
    dpi = int(config_data_dict["image 2D"]['dpi'])
    fig_width_mm = int(config_data_dict["image 2D"]['fig_width_mm'])
    fig_height_mm = int(config_data_dict["image 2D"]['fig_height_mm'])

    background_color = eval(config_data_dict["couleurs image"]['background_color']) # Évaluation de la chaîne comme une expression Python
    line_color = eval(config_data_dict["couleurs image"]['line_color'])
    station_color = eval(config_data_dict["couleurs image"]['station_color'])

    # show configuration data 
    print("Configuration data :") 
    print("----------------------------------")
    print("[site]")

    # on force la première lette du nom de la ville en majuscule pour les recherches dans OSM 
    print("place name:", place_name)

    print("\n[image 2D]")
    print("image_folder:", image_folder)
    print("Image file name : ", output_image_file_name) 
    print("extension_file_format:", extension_file_format)
    print("file_size:", file_size)
    print("dpi:", dpi)
    print("fig_width_mm:", fig_width_mm)
    print("fig_height_mm:", fig_height_mm)

    print("\n[couleurs image]")
    print("background_color:", background_color)
    print("line_color:", line_color)
    print("station_color:", station_color)

    # convert size in mm  
    un_pouce_mm = 25.4 # mm
    fig_width_inches = fig_width_mm / un_pouce_mm
    fig_height_inches = fig_height_mm / un_pouce_mm 

    # test image file folder exists and create it if necessary 
    if not os.path.exists(image_folder):
        # create sub-folder 
        os.makedirs(image_folder)
        print(f"sub-folder : {image_folder} created. ")
    else:
        print(f"sub-folder : {image_folder} already exists.")

    # create full path name with file extension      
    file_path = f"./{image_folder}/{output_image_file_name}.{extension_file_format}"

    # Définir la zone d'étude 
    # place_name = "Rennes"

    # type de transports
    # todo : ajouter dans le fichier de configuration .ini 
    transportation_type = "subway"  # => test ok 
    # transportation_type = "bus"  # => some bugs to be analysed...  
    # transportation_type = "tram" # sur Nantes => extraction de 10 relations dans les 2 sens 
    # transportation_type = "rail" # sur Rennes => aucun résultat 
    # transportation_type = "railway" # => ne fonctionne pas dans dans ce cas la relation n'a pas de clé "from" (et "to")  

    # create list to store line data 
    metro_lines_info = []
    
    print("")
    print("Sending overpass query.") 
    # overpass query for data extraction   
    try:
        data = overpass_request(place_name, transportation_type)
        # print(data)
    except Exception as e:
        print("Error") 
        print(e)
        sys.exit(1)

    # test of data content 
    if not data or 'elements' not in data or not data['elements'] or len(data['elements']) == 0:
        print("Data extraction ERROR !") 
        print("data is empty")
        print("or elements key is not define in data dict.") 
        print("or data[""elements""] is empty.") 
        print("Completd") 
        sys.exit() 
        
    # convert data dict  in dataframe 
    print("Convert data to dataframe format. ") 
    df_raw_data = pd.DataFrame(data["elements"])
       
    # Export DataFrame to CSV file. delimiter = ";" 
    print("Dataframe export into file : {}.".format(output_file)) 
    df_raw_data.to_csv(output_file, sep=';', index=False)

    # data analysis  
    # ------------- 
    # call function line_extraction 
    # return to list : metro_lines_info  
    metro_lines_info = line_extraction(data) 

    # convert extracted data list to pandas DataFrame 
    print("\`nCreate a pandas DataFrame...")
    df_line_info = pd.DataFrame(metro_lines_info)

    # identification des stations de corespondance 
    # Identifier les stations communes entre les lignes
    # Création d'une table croisée pour compter le nombre de lignes par station
    # on traite pour chaque ligne, les 2 sens de circulation. 
    # il faudra donc diviser par 2 les résultats pour ne considérer qu'une seule ligne 
    # avec un seul sens de circulation 
    df_station_counts = df_line_info.pivot_table(index="station_name", columns="line_label", aggfunc='size', fill_value=0)

    # Identification des stations communes
    # ATTENTION : la somme doit être supérieure à 2 
    # car le dataframe contient pour chaque ligne, les 2 sens de circulation 
    df_common_stations = df_station_counts[df_station_counts.sum(axis=1) > 2].index

    # Ajouter la colonne "crossing"
    df_line_info["crossing"] = df_line_info["station_name"].apply(lambda x: "yes" if x in df_common_stations else "no")

    # create dataframe containing station with crossing lines 
    df_crossing_lines_and_stations = df_line_info[df_line_info['crossing'] == 'yes'][['line_label', 'line_name', 'station_name', 'crossing']]
    
    # create dataframe containing for each crossing station, the list of lines 
    df_station_crossing_line_list = df_crossing_lines_and_stations.groupby('station_name')['line_label'].apply(lambda x: list(x.unique())).reset_index()
    
    # rename column "line_label" to "crossing_lines" 
    df_station_crossing_line_list.rename(columns={'line_label': 'crossing_lines'}, inplace=True)
    
    # Fusionner avec le DataFrame original
    # df_crossing_lines = df_crossing_lines.merge(df_line_list, on='station_name', how='left')
    df_line_info = df_line_info.merge(df_station_crossing_line_list, on='station_name', how='left')

    # print(metro_lines_info)
    # show DataFrame
    # print("\nDataFrame :")
    # print(df_line_info)

    # DataFrame export to CSV file 
    print("DataFrame export...")
    try:
        df_line_info.to_csv(output_file_line_info, sep = ";", index=False, encoding='utf-8')
        print(f"Data exportation into file : {output_file_line_info}")
    except Exception as e:
        print("Error : writing CSV file :", str(e))


    # available lines : df_line_info["line_name"].value_counts()
    print("\nLine list : ") 
    print("") 
    # print(df_line_info["line_name"].value_counts()) 

    # line extraction frome df_line_info  
    df_line_list = df_line_info.groupby([ 'line_label', 'line_name']).size().reset_index(name='counts')
    nombre_de_ligne = df_line_list.shape[0]

    print(f"\nExtraction of {nombre_de_ligne} lines.") 
    print("line list : ") 
    print(df_line_list)

    # est_paire = (nombre_de_ligne % 2) == 0

    # extraction of one_line_every_two   
    # 2 circulation ways extracted on the same line 
    # df_one_line_every_two = df_line_list.iloc[::2]
    # print("df_one_line_every_two") 
    # print(df_one_line_every_two) 
     
    # vérification de la présence de l'aller retour
    # df_line_list["line_label"].value_counts()

    # line liste and directions 
    #   df_line_info['line_name'].unique()

    # network plotting 
    # ----------------
        
    print("plot line network, 1 direction per line.") 
    fig = plot_network(df_line_info , fig_width_inches, fig_height_inches, background_color, dpi) 
    
    # send figure to buffer 
    image_base64_buf = plot_to_buffer(fig)
    
    # Save image
    print("Save image file : ", file_path )
    fig.savefig(file_path, dpi=400, bbox_inches="tight", format=extension_file_format)
    
    return image_base64_buf
    # end main function flask IHM

# ----------
#                
# MAIN CODE  
#
# ----------
if __name__ == "__main__":
    
    start_time = datetime.datetime.now()

    main() 
    
    end_time = datetime.datetime.now()

    print("\nProcessing times :")
    print("- Start time :", start_time.strftime('%Y-%m-%d %H h %M m %S s'))    
    print("- End time :", end_time.strftime('%Y-%m-%d %H h %M m %S s'))
    print("- Duration : {:.3f} sec".format((end_time-start_time).total_seconds()))

    print("Code version : ", __version__, " of ", __date__ , ".") 
        
    print("Completed.") 
