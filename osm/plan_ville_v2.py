
"""


"""

__version__ = "3.0" 
__date__ = "2024/12/10"

import pandas as pd 
import requests
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import folium 

import sys 

def relations_list_extraction_from_data(data):
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
    # df_line_list = df_line_list.drop(columns=['wheelchair','wikidata', 'wikipedia', 'twitter', 'source', 'start_date'])     
    
    return df_line_list 

# lines ways extraction from data for lines plotting
def ways_extraction_from_datta(data): # => ok 
    """
    ways extraction of list of transportation lines from data produced by overpass request.
    
    this function extracts ways from data . 
    the returned dataframe permits to create a map of the network based on real wyas of the lines. 
    this dataframe contains nodes latitudes and longitudes.
    
    param : 
    -------
        data : OSM data extracted with overpass request 
        
    returns :
    ---------
        df_ways_tracks : Geopandas dataframe containing ways description of each extracted .
                         columns : ['way_name', 'way_id', 'tags', 'geometry']
                         
                         note : coordinates contains a liste of tuples with (latitude and longitude) of each node of the considered way
                          
    """

    # global relations, nodes, ways
    # global relation, way, node  
    # global dic_line_segments 
    
    # relations, ways, and nodes extraction from data 
    relations = {element['id']: element for element in data['elements'] if element['type'] == 'relation'}
    nodes = {element['id']: element for element in data['elements'] if element['type'] == 'node'}
    ways = [element for element in data['elements'] if element['type'] == 'way']
    
    # group by relation (line id)
    dic_line_segments = {}
    
    # get relations list 
    # df_relations_list = relations_list_extraction_from_data(data) 
    
    # loop on ways 
    for way in ways:
        # print("Way ID : ", way['id'], " - ", way.keys()) 
        
        # get way name in way attributes 
        way_name = way.get('tags', {}).get('name', 'Unknown way')
        way_id = way['id'] 
        # way_public_transport = way.get('tags', {}).get('public_transport', 'Unknown')
        way_tags = way.get('tags', {})
        
        # is it a new way ?
        if way_id not in dic_line_segments:
            dic_line_segments[way_id] = {
                "way_name": way_name,
                "way_id": way_id,
                "tags": way_tags, 
                "coordinates": []
            }
        
        # get nodes coordonnates 
        coordinates = []
        # analysis of nodes list contained in the way 
        for node_id in way.get('nodes', []):
            # get node data from it's id  
            node = nodes.get(node_id)
            if node:
                # add node coordinnates 
                coordinates.append((node['lat'], node['lon']))
        
        # add to dictionnary 
        dic_line_segments[way_id]["coordinates"].extend(coordinates)
    
    # convert dic to DataFrame
    df_ways_tracks = pd.DataFrame.from_records([
        {"way_name": info["way_name"], "way_id": info["way_id"], "tags": info["tags"],  "coordinates": info["coordinates"]}
        for info in dic_line_segments.values()
    ])
    
    # create latitude and logitude columns from coordinaites 
    # Extraction of nodes listes latitude and longitudes
    # df_ways_tracks['latitude'] = df_ways_tracks['coordinates'].apply(lambda coords: [point[0] for point in coords])
    # df_ways_tracks['longitude'] = df_ways_tracks['coordinates'].apply(lambda coords: [point[1] for point in coords])
    
    # delete coordinates column  
    # df_ways_tracks = df_ways_tracks.drop(columns=['coordinates'])

    # Convertir les listes de tuples (latitude, longitude) en LineString
    df_ways_tracks['geometry'] = df_ways_tracks['coordinates'].apply(
                            lambda coord_list: LineString([(lon, lat) for lat, lon in coord_list])  # (longitude, latitude)
                           )

    # Créer un GeoDataFrame
    # Créer un GeoDataFrame
    gdf_ways = gpd.GeoDataFrame(df_ways_tracks, geometry='geometry')
    
    # remove "coordinates" column 
    gdf_ways = gdf_ways.drop(columns=['coordinates'])

    # Définir le système de coordonnées (ici WGS 84)
    gdf_ways.set_crs(epsg=4326, inplace=True) # est le système de référence géographique standard basé sur WGS 84
       
    return gdf_ways 

def overpass_request_location_and_radius(latitude, longitude, radius): 
    """
    Overpass request from location and radius data 
    """
    # overpass URL 
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Requête Overpass
    query = f"""
    [out:json];
    (
      way["highway"~"primary|secondary|tertiary|cycleway|footway"](around:{radius}, {latitude}, {longitude});
      node(around:{radius}, {latitude}, {longitude});
      relation["type"="route"](around:{radius}, {latitude}, {longitude});
    );
    out body;
    >;
    out skel qt;
    """

    print("overpass resuest : ")
    print(query) 
    print("")
    
    # Récupération des données via Overpass API
    response = requests.get(overpass_url, params={"data": query})

    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête : {response.status_code}")

    data = response.json()
    
    return data 

if __name__ == "__main__": 
    # Paramètres pour la requête Overpass
    radius = 100  # rayon en mètres
    # Rennes 
    # latitude = 48.117266  # Exemple : Rennes
    # longitude = -1.677792
    # betton 
    latitude = 48.1871  # degre 
    longitude = -1.6421 # degre 

    print(f"Radius : {radius} m ") 
    print(f"Latitude : {latitude} ° ")
    print(f"Longitude : {longitude} ° ") 

    # data request 
    data = overpass_request_location_and_radius(latitude, longitude, radius) 
    
    # ways extraction from data to geodataframe 
    gdf_ways = ways_extraction_from_datta(data)

    # Tracé de la géométrie
    print("WAYS")
    print("plot gdf_ways")
    gdf_ways.plot(figsize=(10, 10), edgecolor='blue', linewidth=1)

    # Ajouter des titres et étiquettes
    plt.title("Plan des chemins à partir des données geometry")
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.grid(True)

    # Afficher la carte
    plt.show(block = False) 

    # creation d'une carte html avec folluim
    print("plot folium")
    # Reprojeter en CRS projeté pour calculer correctement le centroïde (si nécessaire)
    gdf_ways_projected = gdf_ways.to_crs(epsg=3857)  # CRS projeté, ici Web Mercator
    center = gdf_ways_projected.geometry.centroid.to_crs(epsg=4326).iloc[0].y, \
             gdf_ways_projected.geometry.centroid.to_crs(epsg=4326).iloc[0].x

    # Créer une carte Folium centrée sur le point calculé
    m = folium.Map(location=center, zoom_start=15)

    # Ajouter les géométries (lignes) sur la carte
    for _, row in gdf_ways.iterrows():
        coords = [(lat, lon) for lon, lat in row.geometry.coords]  # latitude, longitude
        folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)

    # Afficher la carte si dans Jupyter
    # m
    m.save("carte_interactive.html")
    
    print("Carte enregistrée dans le fichier 'carte_interactive.html'. Ouvrez ce fichier pour la voir.")

    # Création de la carte avec Cartopy
    # fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': ccrs.PlateCarree()})
    # ax.set_extent([longitude - 0.01, longitude + 0.01, latitude - 0.01, latitude + 0.01])
    # for way in df_ways.iterrows(): 
        # ax.plot(way["longitude"], way["latitude"]) 
    
    #plt.show(black = False) 
    
    
    # STEP 2 : autre algo pour le traitement des  nodes 
    print("NODES") 
    # Transformation en GeoDataFrames
    nodes_data = []
    ways_data = []
    relations_data = []

    nodes = {element['id']: element for element in data['elements'] if element['type'] == 'node'}

    for element in data['elements']:
        if element['type'] == 'node':
            nodes_data.append({
                'id': element['id'],
                'name': element.get('tags', {}).get('name'),
                'tags': element.get('tags', {}),
                'geometry': Point(element['lon'], element['lat'])
            })
        elif element['type'] == 'way':
            nodes_coords = [
                (nodes[node_id]['lon'], nodes[node_id]['lat']) for node_id in element.get('nodes', []) if node_id in nodes
            ]
            ways_data.append({
                'id': element['id'],
                'name': element.get('tags', {}).get('name'),
                'tags': element.get('tags', {}),
                'nodes': element.get('nodes', {}),
                'geometry': LineString(nodes_coords) if nodes_coords else None
            })
        elif element['type'] == 'relation':
            relations_data.append({
                'id': element['id'],
                'name': element.get('tags', {}).get('name'),
                'tags': element.get('tags', {}),
                'members': element.get('members', []),
                'geometry': None  # Les relations complexes nécessitent une gestion spécifique
            })

    # Création des GeoDataFrames
    nodes_gdf = gpd.GeoDataFrame(nodes_data, crs="EPSG:4326")
    ways_gdf = gpd.GeoDataFrame(ways_data, crs="EPSG:4326")
    relations_gdf = gpd.GeoDataFrame(relations_data, crs="EPSG:4326")

    # Filtrage des données pour les couches spécifiques
    filtered_nodes = nodes_gdf[nodes_gdf['tags'].notna()]
    filtered_ways = ways_gdf[ways_gdf['tags'].notna()]

    print("plot nodes") 
    # Création de la carte avec Cartopy
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([longitude - 0.01, longitude + 0.01, latitude - 0.01, latitude + 0.01])

    # Ajout des couches à la carte
    # Routes et pistes cyclables
    filtered_ways.plot(ax=ax, edgecolor='blue', linewidth=1, label='Routes et Pistes')

    # Points d'intérêt
    filtered_nodes.plot(ax=ax, color='red', markersize=10, label='Points d\'intérêt')

    # Ajout des traits de base
    ax.add_feature(cfeature.STATES, edgecolor='gray')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Légende et titre
    plt.legend()
    plt.title("Plan multicouche avec Cartopy")
    plt.show(block=True)

    print("Terminé")



