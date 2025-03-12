import requests
import json


#~DATA 
__version__ = "1.0"
__date__ = "26/02/2025"
__status__ = "ok"
__authors__ = "François, Stéphane et Gabriel" 
__organization__ = "My Human Kit - Rennes, France" 
__licence__ = "CeCILL v2.1 / CC by SA"


def osm_get_indirect_node (streetmap_data, node_id):
    """
    Retrieve an indirect node from the street information dictionary.

    Args:
        transport_info (dict): A dictionary containing osm street information, including nodes.
        node_id (int): The ID of the node to retrieve.

    Returns:
        dict: The node information corresponding to the given node ID.
    """
    return streetmap_data['nodes'][node_id]
def osm_get_indirect_way (streetmap_data, way_id):
    """
    Retrieve an indirect node from the street information dictionary.

    Args:
        transport_info (dict): A dictionary containing osm street information, including nodes.
        node_id (int): The ID of the node to retrieve.

    Returns:
        dict: The node information corresponding to the given node ID.
    """
    return streetmap_data['ways'][way_id]

def overpass_request(latitude, longitude, radius):
    """
    Overpass request from location and radius data 
    """
    # overpass URL 
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Requête Overpass
    #way["highway"~"^(trunk|primary|secondary|tertiary|unclassified|residential)$"](around:{radius}, {latitude}, {longitude});
    query = f"""
    [out:json];
    (
    
    way["highway"](around:{radius}, {latitude}, {longitude});
    wr["building"](around:{radius}, {latitude}, {longitude});
    wr["water"](around:{radius}, {latitude}, {longitude});
    wr["natural"="water"](around:{radius}, {latitude}, {longitude});
    );
    (._;>;);
    
    out body;
    >;
    
    
    """

    print("overpass request : ")
    print(query) 
    print("")
    
    # Récupération des données via Overpass API
    response = requests.get(overpass_url, params={"data": query})

    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête : {response.status_code}")

    data = response.json()
    
    #json.dump (data, open ("overpass_street.json", "w"))
    return data 

def osm_extraction (streetmap_data):

    street_info = {"relations":{},"ways":{}, "nodes":{}} 
   
    if 'elements' not in streetmap_data:
        print("Aucune donnée récupérée pour la ville ")
        return street_info
    else:
        for element in streetmap_data['elements']:
            #print (element['type'])
            if element['type'] == 'relation':
                street_info['relations'][element['id']] = element
            elif element['type'] == 'way':
                street_info['ways'][element['id']] = element
            elif element['type'] == 'node':
                street_info['nodes'][element['id']] = element
            else:
                print ("Type de données non géré : ", element['type'])
    return street_info

def extract_node_from_osmwaynodes (streetmap_data, way):
    nodes = []
    for nodeid in way["nodes"]:
        node = osm_get_indirect_node (streetmap_data, nodeid)
        if "lat" in node and "lon" in node:
            anoted_node = {
                "lat": node["lat"],
                "lon": node["lon"],
                "id": node["id"],
                "way_id": way["id"],
                
            }
            nodes.append (anoted_node)
    return (nodes)       
 
def osm_extract_data (streetmap_data):
    streetmap_2d_data = {"street":[],"building":[], "unclassified":[], "water":[]}
    ways = []
    for relation in streetmap_data['relations'].values():
        if "tags" in relation:
            if "natural" in relation["tags"]:
                print ("water polygon detected")
                if relation["tags"]["natural"] == "water":
                    for member in relation['members']:
                        if 'type' in member:
                            if member['type'] == 'way':
                                if 'role' in member:
                                    if member['role'] == 'outer':
                                        way = osm_get_indirect_way (streetmap_data, member['ref'])
                                        ways_node = []
                                        if "nodes" in way:
                                            ways_node = extract_node_from_osmwaynodes (streetmap_data, way)
                                            
                                            water = {
                                                "id": way['id'],
                                                "water": "polygon",
                                                "nodes":ways_node
                                            }
                                            streetmap_2d_data["water"].append (water)
                                    
            elif "building" in relation["tags"]:
                if 'members' in relation:
                    for member in relation['members']:
                        if 'type' in member:
                            if member['type'] == 'way':
                                if 'role' in member:
                                    if member['role'] == 'outer':
                                        way = osm_get_indirect_way (streetmap_data, member['ref'])
                                        ways_node = []
                                        if "nodes" in way:
                                            ways_node = extract_node_from_osmwaynodes (streetmap_data, way)
                                            
                                            building = {
                                                "id": way['id'],
                                                "building": "polygon",
                                                "nodes":ways_node
                                            }
                                            streetmap_2d_data["building"].append (building)

    for way in streetmap_data['ways'].values():
        ways_node = []
        if 'tags' in way:
            if 'highway' in way['tags']:
                
                #build a street
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                            #if "tags" in node:
                            #    print (node['tags'])
                            anoted_node = {
                                "lat": node["lat"],
                                "lon": node["lon"],
                                "id": node["id"],
                                "way_id": way["id"],
                                
                            }
                            ways_node.append (anoted_node)
                    
                    street = {
                        "id": way['id'],
                        "highway": way['tags']['highway'],
                        "nodes":ways_node,
                        "tags": way['tags'] #conserve tags for width estimation
                    }
                    streetmap_2d_data["street"].append (street)

            elif 'building' in way['tags']:
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                            anoted_node = {
                                    "lat": node["lat"],
                                    "lon": node["lon"],
                                    "id": node["id"],
                                    "way_id": way["id"],
                                    
                                }
                            ways_node.append (anoted_node)
                        
                    building = {
                        "id": way['id'],
                        "building": way['tags']['building'],
                        "nodes":ways_node
                    }
                    streetmap_2d_data["building"].append (building)

            elif "water" in way['tags']:
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                                anoted_node = {
                                    "lat": node["lat"],
                                    "lon": node["lon"],
                                    "id": node["id"],
                                    "way_id": way["id"],
                                    
                                }
                                ways_node.append (anoted_node)
                        
                    water = {
                        "id": way['id'],
                        "water": way['tags']['water'],
                        "nodes":ways_node
                    }
                    streetmap_2d_data["water"].append (water)
            else:
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                                anoted_node = {
                                    "lat": node["lat"],
                                    "lon": node["lon"],
                                    "id": node["id"],
                                    "way_id": way["id"],
                                    
                                }
                                ways_node.append (anoted_node)
                        
                    unclassified = {
                        "id": way['id'],
                        "tags": way.get ("tags", []),
                        "nodes":ways_node
                    }
                    streetmap_2d_data["unclassified"].append (unclassified)

    return streetmap_2d_data