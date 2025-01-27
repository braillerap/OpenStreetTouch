
"""


"""

import requests
import pandas as pd
import matplotlib.pyplot as plt

import sys 
sys.stdout.reconfigure(encoding='utf-8') 

relations = None 
relation = None 
ways = None 
way = None
nodes = None 
node = None
dic_lines_ways = {}

dic_line_segments = None 
df_line_list = None

# fonction d'extraction des données avec overpass (rien de changé) 
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
    place_name = place_name.title().strip() 
    
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

def lines_list_extraction_from_data(data):  # => ok 
    """
    Extraction of list of transportation lines from data produced by overpass request.
    
    param : 
        data : data extracted by overpass request 
        
    returns :
    ---------
        df_line_list : pandas dataframe containing relation["tag"] of each extracted line. 
    """
    
    global df_line_list 
    
    # relations extraction from data 
    relations = {element['id']: element for element in data['elements'] if element['type'] == 'relation'} 
    
    df_line_list = pd.DataFrame() 
    
    for relation_id, relation in relations.items():
        # get line info 
        df_new_row = pd.DataFrame([relation["tags"]])        
        df_line_list = pd.concat([df_line_list, df_new_row], ignore_index=True)
    
    # columns : ['colour', 'description', 'from', 'interval', 'interval:peak', 'name',
    #   'network', 'network:wikidata', 'note', 'opening_hours', 'operator',
    #   'public_transport:version', 'ref', 'ref:FR:STAR', 'route',
    #    'text_colour', 'text_colour:style', 'to', 'type', 'wheelchair',
    #   'wikidata', 'wikipedia', 'twitter', 'source', 'start_date']
    df_line_list = df_line_list.drop(columns=['wheelchair','wikidata', 'wikipedia', 'twitter', 'source', 'start_date'])     
    
    return df_line_list 
           
# lines ways extraction from data 
def lines_ways_extraction_from_datta(data): # => coquille vide en prévision d'y mettre le bon algo... 
    """
    ways extraction of list of transportation lines from data produced by overpass request.
    
    this function extracts ways associated to each relation describing a transportation line. 
    the returned dataframe permits to create a map of the network based on real wyas of the lines. 
    
    param : 
        data : data extracted by overpass request 
        
    returns :
    ---------
        df_line_ways : pandas dataframe containing ways of each extracted line relation.
                       columns : ['line_name', 'line_description', 'line_from', 'line_to', 'line_id', 'ways_id_list']        
    """
   
# 
def data_extraction_lines_proto(data): # => PROTOTYPE 
    """
    relations, ways, and nodes extraction from data to get lines traces 
    """    
    
    print("fonction ; data_extraction_lines_proto")
    global relations, nodes, ways
    global relation, way, node  
    global dic_line_segments 
    
    # Extraction des tracés
    relations = {element['id']: element for element in data['elements'] if element['type'] == 'relation'}
    nodes = {element['id']: element for element in data['elements'] if element['type'] == 'node'}
    ways = [element for element in data['elements'] if element['type'] == 'way']
    
    # Regrouper par relation (identifiant de ligne)
    dic_line_segments = {}
    
    # get line list 
    df_line_list = lines_list_extraction_from_data(data) 
    
    # get ways list 
    # df = lines_ways_extraction_from_datta(data) 
    
    # print("\nWAYS\n")
    
    for way in ways:
        # print("Way ID : ", way['id'], " - ", way.keys()) 
        
        # Récupérer le nom de la ligne
        line_name = way.get('tags', {}).get('name', 'Ligne inconnue')
        way_id = way['id']  # Vous pouvez utiliser 'id' ou d'autres tags pour identifier le way
        # print("\nway : ")
        # print("=> ", way_id, line_name)
        # print("way : ", way) 
        
        
        if way_id not in dic_line_segments:
            dic_line_segments[way_id] = {
                "line_name": line_name,
                "way_id": way_id,
                "coordinates": []
            }
        
        # Récupérer les coordonnées
        coordinates = []
        # parcours des identifants des nodes dans l'objet way 
        for node_id in way.get('nodes', []):
            # récupération du node à partir de son identifiant 
            node = nodes.get(node_id)
            if node:
                coordinates.append((node['lat'], node['lon']))
        
        dic_line_segments[way_id]["coordinates"].extend(coordinates)
    
    # Conversion en DataFrame
    df_line_tracks = pd.DataFrame.from_records([
        {"line_name": info["line_name"], "way_id": info["way_id"],  "coordinates": info["coordinates"]}
        for info in dic_line_segments.values()
    ])
    
    # création de deux colonnes latitude et longitude dans le cataframe à partir de la colonne coordonates
    # Extraction des listes de latitudes et de longitudes
    df_line_tracks['latitude'] = df_line_tracks['coordinates'].apply(lambda coords: [point[0] for point in coords])
    df_line_tracks['longitude'] = df_line_tracks['coordinates'].apply(lambda coords: [point[1] for point in coords])

    # print("df_line_tracks : ") 
    # print(df_line_tracks) 
    
    return df_line_tracks 

def plot_lines(df_raw_data):
    """
    Fonction pour tracer les lignes de métro à partir d'un DataFrame
    
    Parameters:
    ------------
        df_raw_data : DataFrame pandas contenant les données de lignes ['line_name', 'way_id', 'coordinates', 'latitude', 'longitude'], dtype='object'
    """
    #plt.figure(figsize=(10, 8))
    
    for index, row in df_raw_data.iterrows():
        # nouvelle courbe pour chqua way 
        plt.figure(figsize=(10, 8))
        
        # Récupérer les coordonnées
        coords = row['coordinates']
        if coords:
            # Séparer les latitudes et longitudes
            latitudes, longitudes = zip(*coords)
            # Tracer la ligne
            plt.plot(longitudes, latitudes, label=row['line_name'])
    
    plt.show(block = False)
    
    # Ajouter des légendes et un titre
    #plt.title("Lignes de métro à Rennes")
    #plt.xlabel("Longitude")
    #plt.ylabel("Latitude")
    #plt.legend()
    #plt.grid()
    #plt.show(block = False)
    return 
    
if __name__ == "__main__":
    place_name = "Rennes"
    # data request 
    data = overpass_request (place_name)
    
    relations = {element['id']: element for element in data['elements'] if element['type'] == 'relation'} 
    
    # list of lines extracted 
    df_lines_list = lines_list_extraction_from_data(data) 
    
    # line tracks extraction 
    print("\nPROTO for line tracks extraction :") 
    df_line_tracks_proto = data_extraction_lines_proto(data) 
    # nb_of_nodes_proto = [len(df_line_tracks_proto["coordinates"][k]) for k in df_line_tracks_proto.index]
    
    # valeurs_uniques = df_line_tracks['line_name'].unique()
    #print("\nnoms des vays : ")
    #print(valeurs_uniques)
    print("")
    
    # tracé des lignes 
    print("Tracé des lignes ")
    # plot_lines(df_line_tracks_proto) 
    
    #////////////////
    #
    #  autre version 
    #
    # mise au point fonction extraction traks and nodes of ways 
    # /////////////////////////////////////////////////
    print("\nDEV : test nouvelle version pour l'extraction des ways ") 
    # init dictionnary to store ways as line component 
    dic_line_ways = {}
    
    # init dictionnary to store way points as line component
    dic_line_waypoints = {} 
    
    # pandas dataframe to store ways for each line 
    df_line_ways_list = pd.DataFrame()
    df_line_tracks = pd.DataFrame()

    # step 1 : analyse of relations for ways identification 
    # -----------------------------------------------------
    for element in data['elements']:
        # extract new relation and associated ways for line tracing 
        if element['type'] == 'relation' and 'tags' in element:
            # get line name or identifer 
            print("get line name or identifer") 
            line_id = element['id']
            line_name = element['tags'].get('name', f"Ligne {line_id}")
            line_description = element['tags'].get('description', f"No description")
            line_from = element['tags'].get('from', "")
            line_to = element['tags'].get('to', "")
            line_ref = element['tags'].get('ref', "")
            print("") 
            print("line : ", line_id, " - ", line_name, " - ", line_description) 
            
            # init ist of ways for this line
            dic_line_ways["line_name"] = line_name
            dic_line_ways["line_description"] = line_description
            dic_line_ways["line_from"] = line_from 
            dic_line_ways["line_to"] = line_to 
            dic_line_ways["line_id"] = line_id 
            dic_line_ways["ways_id_list"] = [] # to store liste or ways Ids
            
            # analyse way members of selected relation
            for member in element.get('members', []):
                # is membrr a un way ?
                if member['type'] == 'way':
                    # add way identifier to the list
                    # print("MEMBER line_id : ", line_id, "member : ", member['ref']) 
                    dic_line_ways["ways_id_list"].append(member['ref'])
                
                # add the dictionnary to a pandas dataframe as new row 
                df_new_row = pd.DataFrame([dic_lines_ways])
            
            #print("Dic : ")
            #print(dic_line_ways) 
            
            # add new row to dataframe to store ways associated to each line 
            df_new_row =  pd.DataFrame([dic_line_ways])
            df_line_ways_list = pd.concat([df_line_ways_list, df_new_row], ignore_index=True)

    # print("df_line_ways_list") 
    # print(df_line_ways_list) 
    
    # step 2 : extract waypoints of ways tracks associated to relations 
    # -----------------------------------------------------------------
    # print("STEP 2") 
    
    # extract list of ways with details from exctrated data 
    # extract list of ways in a dictionnary with details from exctrated data
    ways_dic = {element['id']: element for element in data['elements'] if element['type'] == 'way'}
    
    # extract list of nodes in a dictionnary with details from exctrated data 
    nodes_dic = {element['id']: element for element in data['elements'] if element['type'] == 'node'}
        
    # loop on each line to get ways ids and associated waypoints (nodes)
    # use df_line_ways_list
    for index, row in df_line_ways_list.iterrows():
        # use dic_line_waypoints for each line (i.e. relation) 
        waypoints_coordinates = []
        waypoints_latitude = []
        waypoints_longitude = []
        line_name = row['line_name']
        line_id = row['line_id']
         
        dic_line_waypoints["line_name"] = line_name 
        dic_line_waypoints["line_id"] = line_id 
        
        # ways id of current line (i.e. relation) 
        ways_id_list = row['ways_id_list']
        # print("") 
        # print(f"\nTraitement de la ligne : ", dic_line_waypoints["line_name"])
        # print("Nb de wyas id : ", len(ways_id_list)) 
        # extractions of ways detailled information 
        # => crete a dictionnary with filtered ways corresponding to ways_id_list 
        filtered_ways_dic = {key: way for key, way in ways_dic.items() if way['id'] in ways_id_list}
        # filtered_ways_dic = ways_dic 
        # first_item = next(iter(filtered_ways_dic.items()))
 
        # nodes_dic_of_filtered_ways = {way['nodes'] for way in filtered_ways_dic.values()}
        # FLB 
        # filtered_nodes_dic = {k: v for k, v in filtered_ways_dic.items() if isinstance(v.get("nodes"), list)}
        
        k = 0 # way compter 
        # loop on way ids from "ways_id_list"
        for way in filtered_ways_dic.values():
            k = k + 1
            # print("\n => Segment ID: ", k, " - ", way["id"])
            # print("Nb of nodes : ", len(way.get('nodes', []))) 
            nb_nodes = 0  # node compter 
            
            # parcours des nodes dans liste des filtered ways  
            for node_id in way.get('nodes', []):  # way.get('nodes', []) is a list 
                nb_nodes = nb_nodes + 1
                node = nodes_dic.get(node_id)
                # print("node index : ", nb_nodes , " - Node object : ", node)
                if node:
                    waypoints_coordinates.append((node['lat'], node['lon']))
                    waypoints_latitude.append(node['lat'])
                    waypoints_longitude.append(node['lon'])
                    
                    # print("coord : ", waypoints_coordinates, " len : ", len(waypoints_coordinates)) 
        
        # add list of waypoints coordonnates in kictionnary describing current line 
        dic_line_waypoints["coordinates"] = waypoints_coordinates
        dic_line_waypoints["latitude"] = waypoints_latitude 
        dic_line_waypoints["longitude"] = waypoints_longitude 
        # add dic_line_waypoints to dataframe 
        df_new_line_row = pd.DataFrame([dic_line_waypoints])
        df_line_tracks = pd.concat([df_line_tracks, df_new_line_row], ignore_index=True)
         
    # determination du nombre de nodes pour chaque ligne 
    nb_of_nodes = [len(df_line_tracks["coordinates"][k]) for k in df_line_tracks.index]
    
    # print("Exit....")
    # sys.exit()
    
    # plot network 
    # print("line tracks") 
    #if data is not None:
    #    # plot_lines(df_line_tracks)
    
    # tracé des lignes avec df_line_tracks
    # print("\main : Tracé des lignes... ") 
    
    #for index, row in df_line_tracks.iterrows():
    #    plt.figure(figsize=(10, 8))
    #    # Récupérer les coordonnées
    #    coords = row['coordinates']
    #    lat = row['latitude']
    #    lon = row['longitude']
    #    #print("cordonnée : ", coords)
    #    if coords:
            # Séparer les latitudes et longitudes
    #        #latitudes, longitudes = zip(*coords)
    #        #print("Lat : ", latitudes)
    #        #print("Long : ", longitudes)
    #        # Tracer la ligne
    #        # plt.plot(lon, lat, label=row['line_name'])
    #        # Créer les subplots : 2 lignes, 1 colonne
    #        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))

            # Premier subplot
    #        ax1.plot(lon, label="longitude")
    #        ax1.set_title("Premier subplot")
    #        ax1.set_ylabel("Longitude")
            
            # Second subplot
    #        ax2.plot(lat, label="latitude", color='blue')  # Couleur différente pour exemple
    #        # ax2.set_title("Second subplot")
    #        ax2.set_ylabel("Latitude")
            
            # Affichage
    #        plt.tight_layout()  # Ajuste l'espacement entre les subplots

        # Ajouter des légendes et un titre
        #plt.title("Lignes de métro à Rennes")
        #plt.xlabel("Longitude")
        #plt.ylabel("Latitude")
        #plt.legend()
        #plt.grid()
    #    plt.show(block = False)
    
# Séparation des latitudes et longitudes
# latitudes = [coord[0] for coord in coords]
# longitudes = [coord[1] for coord in coords]

# Création du tracé
#plt.figure(figsize=(10, 8))
#plt.plot(longitudes, latitudes, marker='o', color='b', linestyle='-', markersize=5, label="Trajet")

# Ajout des étiquettes et titre
#plt.xlabel("Longitude")
#plt.ylabel("Latitude")
#plt.title("Tracé des positions géographiques")
#plt.legend()
#plt.grid(True)

# Affichage du graphique
#plt.show()

print("Terminé")
